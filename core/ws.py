"""
WebSocket 核心通信模块

该模块定义了 `WS` 类，负责与 OneBot v11 实现（如 NapCat）建立和管理
WebSocket 连接。它是整个机器人框架的底层通信基础。

主要职责包括：
- 建立 WebSocket 连接并处理认证。
- 实现断线自动重连机制。
- 监听并接收来自 OneBot 的事件和 API 响应。
- 分发事件给 `CommandManager` 进行处理。
- 提供 `call_api` 方法，用于异步发送 API 请求并等待响应。
"""
import asyncio
import json
import traceback
import uuid
from datetime import datetime

import websockets

from models import EventFactory

from .bot import Bot
from .command_manager import matcher
from .config_loader import global_config
from .logger import logger


class WS:
    """
    WebSocket 客户端，负责与 OneBot v11 实现进行底层通信。
    """

    def __init__(self):
        """
        初始化 WebSocket 客户端。

        从全局配置中读取 WebSocket URI、访问令牌（Token）和重连间隔。
        """
        # 读取参数
        cfg = global_config.napcat_ws
        self.url = cfg.get("uri")
        self.token = cfg.get("token")
        self.reconnect_interval = cfg.get("reconnect_interval", 5)

        self.ws = None
        self._pending_requests = {}
        self.bot = Bot(self)

    async def connect(self):
        """
        启动并管理 WebSocket 连接。

        这是一个无限循环，负责建立连接。如果连接断开，它会根据配置的
        `reconnect_interval` 时间间隔后自动尝试重新连接。
        """
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

        while True:
            try:
                logger.info(f"正在尝试连接至 NapCat: {self.url}")
                async with websockets.connect(
                    self.url, additional_headers=headers
                ) as websocket:
                    self.ws = websocket
                    logger.success("连接成功！")
                    await self._listen_loop(websocket)

            except (
                websockets.exceptions.ConnectionClosed,
                ConnectionRefusedError,
            ) as e:
                logger.warning(f"连接断开或服务器拒绝访问: {e}")
            except Exception as e:
                logger.exception(f"运行异常: {e}")

            logger.info(f"{self.reconnect_interval}秒后尝试重连...")
            await asyncio.sleep(self.reconnect_interval)

    async def _listen_loop(self, websocket):
        """
        核心监听循环，处理所有接收到的 WebSocket 消息。

        此循环会持续从 WebSocket 连接中读取消息，并根据消息内容
        判断是 API 响应还是上报的事件，然后分发给相应的处理逻辑。

        Args:
            websocket: 当前活动的 WebSocket 连接对象。
        """
        async for message in websocket:
            try:
                data = json.loads(message)

                # 1. 处理 API 响应
                # 如果消息中包含 echo 字段，说明是 API 调用的响应
                echo_id = data.get("echo")
                if echo_id and echo_id in self._pending_requests:
                    future = self._pending_requests.pop(echo_id)
                    if not future.done():
                        future.set_result(data)
                    continue

                # 2. 处理上报事件
                # 如果消息中包含 post_type 字段，说明是 OneBot 上报的事件
                if "post_type" in data:
                    # 使用 create_task 异步执行，避免阻塞 WebSocket 接收循环
                    asyncio.create_task(self.on_event(data))

            except Exception as e:
                logger.exception(f"解析消息异常: {e}")

    async def on_event(self, raw_data: dict):
        """
        事件处理和分发层。

        当接收到一个 OneBot 事件时，此方法负责：
        1. 使用 `EventFactory` 将原始 JSON 数据解析成对应的事件对象。
        2. 为事件对象注入 `Bot` 实例，以便在插件中可以调用 API。
        3. 打印格式化的事件日志。
        4. 将事件对象传递给 `CommandManager` (`matcher`) 进行后续处理。

        Args:
            raw_data (dict): 从 WebSocket 接收到的原始事件字典。
        """
        try:
            # 使用工厂创建事件对象
            event = EventFactory.create_event(raw_data)
            event.bot = self.bot  # 注入 Bot 实例

            # 打印日志
            if event.post_type == "message":
                sender_name = event.sender.nickname if event.sender else "Unknown"
                logger.info(f"[消息] {event.message_type} | {event.user_id}({sender_name}): {event.raw_message}")
            elif event.post_type == "notice":
                logger.info(f"[通知] {event.notice_type}")
            elif event.post_type == "request":
                logger.info(f"[请求] {event.request_type}")
            elif event.post_type == "meta_event":
                logger.debug(f"[元事件] {event.meta_event_type}")


            # 分发事件
            await matcher.handle_event(self.bot, event)

        except Exception as e:
            logger.exception(f"事件处理异常: {e}")

    async def call_api(self, action: str, params: dict = None):
        """
        向 OneBot v11 实现端发送一个 API 请求。

        该方法通过 WebSocket 发送请求，并使用 `echo` 字段来匹配对应的响应。
        它创建了一个 `Future` 对象来异步等待响应，并设置了超时机制。

        Args:
            action (str): API 的动作名称，例如 "send_group_msg"。
            params (dict, optional): API 请求的参数字典。 Defaults to None.

        Returns:
            dict: OneBot API 的响应数据。如果超时或连接断开，则返回一个
                  表示失败的字典。
        """
        if not self.ws:
            logger.error("调用 API 失败: WebSocket 未初始化")
            return {"status": "failed", "msg": "websocket not initialized"}

        from websockets.protocol import State

        if getattr(self.ws, "state", None) is not State.OPEN:
            logger.error("调用 API 失败: WebSocket 连接未打开")
            return {"status": "failed", "msg": "websocket is not open"}

        echo_id = str(uuid.uuid4())
        payload = {"action": action, "params": params or {}, "echo": echo_id}

        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self._pending_requests[echo_id] = future

        await self.ws.send(json.dumps(payload))

        try:
            return await asyncio.wait_for(future, timeout=30.0)
        except asyncio.TimeoutError:
            self._pending_requests.pop(echo_id, None)
            logger.warning(f"API 调用超时: action={action}, params={params}")
            return {"status": "failed", "retcode": -1, "msg": "api timeout"}


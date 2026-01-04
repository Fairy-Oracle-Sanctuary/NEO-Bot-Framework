"""
事件处理器模块

该模块定义了用于处理不同类型事件的处理器类。
每个处理器都负责注册和分发特定类型的事件。
"""
import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple

from .bot import Bot
from .permission_manager import Permission, permission_manager
from .exceptions import SyncHandlerError
from .executor import run_in_thread_pool


class BaseHandler(ABC):
    """
    事件处理器抽象基类
    """
    def __init__(self):
        self.handlers: List[Dict[str, Any]] = []

    @abstractmethod
    async def handle(self, bot: Bot, event: Any):
        """
        处理事件
        """
        raise NotImplementedError

    async def _run_handler(
        self,
        func: Callable,
        bot: Bot,
        event: Any,
        args: Optional[List[str]] = None,
        permission_granted: Optional[bool] = None
    ):
        """
        智能执行事件处理器，并注入所需参数
        """
        sig = inspect.signature(func)
        params = sig.parameters
        kwargs = {}

        if "bot" in params:
            kwargs["bot"] = bot
        if "event" in params:
            kwargs["event"] = event
        if "args" in params and args is not None:
            kwargs["args"] = args
        if "permission_granted" in params and permission_granted is not None:
            kwargs["permission_granted"] = permission_granted

        if inspect.iscoroutinefunction(func):
            result = await func(**kwargs)
        else:
            # 如果是同步函数，则放入线程池执行
            result = await run_in_thread_pool(func, **kwargs)
        return result is True


class MessageHandler(BaseHandler):
    """
    消息事件处理器
    """
    def __init__(self, prefixes: Tuple[str, ...]):
        super().__init__()
        self.prefixes = prefixes
        self.commands: Dict[str, Dict] = {}
        self.message_handlers: List[Callable] = []

    def on_message(self) -> Callable:
        """
        注册通用消息处理器
        """
        def decorator(func: Callable) -> Callable:
            if not inspect.iscoroutinefunction(func):
                raise SyncHandlerError(f"消息处理器 {func.__name__} 必须是异步函数 (async def).")
            self.message_handlers.append(func)
            return func
        return decorator

    def command(
        self,
        name: str,
        permission: Optional[Permission] = None,
        override_permission_check: bool = False
    ) -> Callable:
        """
        注册命令处理器
        """
        def decorator(func: Callable) -> Callable:
            if not inspect.iscoroutinefunction(func):
                raise SyncHandlerError(f"命令处理器 {func.__name__} 必须是异步函数 (async def).")
            self.commands[name] = {
                "func": func,
                "permission": permission,
                "override_permission_check": override_permission_check,
            }
            return func
        return decorator

    async def handle(self, bot: Bot, event: Any):
        """
        处理消息事件，包括通用消息和命令
        """
        for handler in self.message_handlers:
            consumed = await self._run_handler(handler, bot, event)
            if consumed:
                return

        if not event.raw_message:
            return

        raw_text = event.raw_message.strip()
        prefix_found = next((p for p in self.prefixes if raw_text.startswith(p)), None)

        if not prefix_found:
            return

        full_cmd = raw_text[len(prefix_found):].split()
        if not full_cmd:
            return

        cmd_name = full_cmd[0]
        args = full_cmd[1:]

        if cmd_name in self.commands:
            command_info = self.commands[cmd_name]
            func = command_info["func"]
            permission = command_info.get("permission")
            override_check = command_info.get("override_permission_check", False)

            permission_granted = True
            if permission:
                permission_granted = await permission_manager.check_permission(event.user_id, permission)

            if not permission_granted and not override_check:
                await bot.send(event, f"权限不足，需要 {permission.name} 权限")
                return

            await self._run_handler(
                func,
                bot,
                event,
                args=args,
                permission_granted=permission_granted
            )


class NoticeHandler(BaseHandler):
    """
    通知事件处理器
    """
    def register(self, notice_type: Optional[str] = None) -> Callable:
        """
        注册通知处理器
        """
        def decorator(func: Callable) -> Callable:
            if not inspect.iscoroutinefunction(func):
                raise SyncHandlerError(f"通知处理器 {func.__name__} 必须是异步函数 (async def).")
            self.handlers.append({"type": notice_type, "func": func})
            return func
        return decorator

    async def handle(self, bot: Bot, event: Any):
        """
        处理通知事件
        """
        for handler in self.handlers:
            if handler["type"] is None or handler["type"] == event.notice_type:
                await self._run_handler(handler["func"], bot, event)


class RequestHandler(BaseHandler):
    """
    请求事件处理器
    """
    def register(self, request_type: Optional[str] = None) -> Callable:
        """
        注册请求处理器
        """
        def decorator(func: Callable) -> Callable:
            if not inspect.iscoroutinefunction(func):
                raise SyncHandlerError(f"请求处理器 {func.__name__} 必须是异步函数 (async def).")
            self.handlers.append({"type": request_type, "func": func})
            return func
        return decorator

    async def handle(self, bot: Bot, event: Any):
        """
        处理请求事件
        """
        for handler in self.handlers:
            if handler["type"] is None or handler["type"] == event.request_type:
                await self._run_handler(handler["func"], bot, event)

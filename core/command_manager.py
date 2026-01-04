"""
命令与事件管理器模块

该模块定义了 `CommandManager` 类，它是整个机器人框架事件处理的核心。
它通过装饰器模式，为插件提供了注册消息指令、通知事件处理器和
请求事件处理器的能力。
"""
from typing import Any, Callable, Dict, Optional, Tuple

from .config_loader import global_config
from .event_handler import MessageHandler, NoticeHandler, RequestHandler


# 从配置中获取命令前缀
comm_prefixes = global_config.bot.get("command", ("/",))


class CommandManager:
    """
    命令管理器，负责注册和分发所有类型的事件。

    这是一个单例对象（`matcher`），在整个应用中共享。
    它将不同类型的事件处理委托给专门的处理器类。
    """

    def __init__(self, prefixes: Tuple[str, ...]):
        """
        初始化命令管理器。

        Args:
            prefixes (Tuple[str, ...]): 一个包含所有合法命令前缀的元组。
        """
        self.plugins: Dict[str, Dict[str, Any]] = {}
        
        # 初始化专门的事件处理器
        self.message_handler = MessageHandler(prefixes)
        self.notice_handler = NoticeHandler()
        self.request_handler = RequestHandler()

        # 将处理器映射到事件类型
        self.handler_map = {
            "message": self.message_handler,
            "notice": self.notice_handler,
            "request": self.request_handler,
        }

        # 注册内置的 /help 命令
        self._register_internal_commands()

    def _register_internal_commands(self):
        """
        注册框架内置的命令
        """
        # Help 命令
        self.message_handler.command("help")(self._help_command)
        self.plugins["core.help"] = {
            "name": "帮助",
            "description": "显示所有可用指令的帮助信息",
            "usage": "/help",
        }

    # --- 装饰器代理 ---

    def on_message(self) -> Callable:
        """
        装饰器：注册一个通用的消息处理器。
        """
        return self.message_handler.on_message()

    def command(
        self,
        name: str,
        permission: Optional[Any] = None,
        override_permission_check: bool = False
    ) -> Callable:
        """
        装饰器：注册一个消息指令处理器。
        """
        return self.message_handler.command(
            name,
            permission=permission,
            override_permission_check=override_permission_check
        )

    def on_notice(self, notice_type: Optional[str] = None) -> Callable:
        """
        装饰器：注册一个通知事件处理器。
        """
        return self.notice_handler.register(notice_type=notice_type)

    def on_request(self, request_type: Optional[str] = None) -> Callable:
        """
        装饰器：注册一个请求事件处理器。
        """
        return self.request_handler.register(request_type=request_type)

    # --- 事件处理 ---

    async def handle_event(self, bot, event):
        """
        统一的事件分发入口。

        根据事件的 `post_type` 将其分发给对应的处理器。
        """
        if event.post_type == 'message' and global_config.bot.get('ignore_self_message', False):
            if hasattr(event, 'user_id') and hasattr(event, 'self_id') and event.user_id == event.self_id:
                return

        handler = self.handler_map.get(event.post_type)
        if handler:
            await handler.handle(bot, event)

    # --- 内置命令实现 ---

    async def _help_command(self, bot, event):
        """
        内置的 `/help` 命令的实现。
        """
        help_text = "--- 可用指令列表 ---\n"
        
        for plugin_name, meta in self.plugins.items():
            name = meta.get("name", "未命名插件")
            description = meta.get("description", "暂无描述")
            usage = meta.get("usage", "暂无用法说明")
            
            help_text += f"\n{name}:\n"
            help_text += f"  功能: {description}\n"
            help_text += f"  用法: {usage}\n"
            
        await bot.send(event, help_text.strip())


# --- 全局单例 ---

# 确保前缀配置是元组格式
if isinstance(comm_prefixes, list):
    comm_prefixes = tuple(comm_prefixes)
elif isinstance(comm_prefixes, str):
    comm_prefixes = (comm_prefixes,)

# 实例化全局唯一的命令管理器
matcher = CommandManager(prefixes=comm_prefixes)


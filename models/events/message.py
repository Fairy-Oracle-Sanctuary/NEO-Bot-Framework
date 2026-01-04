"""
消息事件模型模块

定义了消息相关的事件类，包括 MessageEvent, PrivateMessageEvent, GroupMessageEvent。
"""
from dataclasses import dataclass, field
from typing import List, Optional

from core.permission_manager import ADMIN, OP, USER
from models.message import MessageSegment
from models.sender import Sender
from .base import OneBotEvent, EventType


@dataclass(slots=True)
class Anonymous:
    """
    匿名信息
    """
    id: int = 0
    """匿名用户 ID"""
    
    name: str = ""
    """匿名用户名称"""
    
    flag: str = ""
    """匿名用户 flag"""


@dataclass
class MessageEvent(OneBotEvent):
    """
    消息事件基类
    """

    # 权限级别常量，用于装饰器参数
    ADMIN = ADMIN
    OP = OP
    USER = USER

    message_type: str
    """消息类型: private (私聊), group (群聊)"""

    sub_type: str
    """
    消息子类型
    如果是私聊消息，可能是 friend, group, other, normal, anonymous, notice
    如果是群聊消息，可能是 normal, anonymous, notice
    """

    message_id: int
    """消息 ID"""

    user_id: int
    """发送者 QQ 号"""

    message: List[MessageSegment] = field(default_factory=list)
    """消息内容列表"""

    raw_message: str = ""
    """原始消息内容"""

    font: int = 0
    """字体"""

    sender: Optional[Sender] = None
    """发送者信息"""

    @property
    def post_type(self) -> str:
        return EventType.MESSAGE

    async def reply(self, message: str, auto_escape: bool = False):
        """
        回复消息（抽象方法，由子类实现）

        :param message: 回复内容
        :param auto_escape: 是否自动转义
        """
        raise NotImplementedError("reply method must be implemented by subclasses")


@dataclass
class PrivateMessageEvent(MessageEvent):
    """
    私聊消息事件
    """

    async def reply(self, message: str, auto_escape: bool = False):
        """
        回复私聊消息

        :param message: 回复内容
        :param auto_escape: 是否自动转义
        """
        await self.bot.send_private_msg(
            user_id=self.user_id, message=message, auto_escape=auto_escape
        )


@dataclass
class GroupMessageEvent(MessageEvent):
    """
    群聊消息事件
    """

    group_id: int = 0
    """群号"""

    anonymous: Optional[Anonymous] = None
    """匿名信息"""

    async def reply(self, message: str, auto_escape: bool = False):
        """
        回复群聊消息

        :param message: 回复内容
        :param auto_escape: 是否自动转义
        """
        await self.bot.send_group_msg(
            group_id=self.group_id, message=message, auto_escape=auto_escape
        )

"""
请求事件模型模块

定义了请求相关的事件类。
"""
from dataclasses import dataclass
from .base import OneBotEvent, EventType


@dataclass(slots=True)
class RequestEvent(OneBotEvent):
    """
    请求事件基类
    """

    request_type: str
    """请求类型"""

    @property
    def post_type(self) -> str:
        return EventType.REQUEST


@dataclass
class FriendRequestEvent(RequestEvent):
    """
    加好友请求事件
    """
    user_id: int = 0
    """发送请求的 QQ 号"""
    
    comment: str = ""
    """验证信息"""
    
    flag: str = ""
    """请求 flag，在调用处理请求的 API 时需要传入此 flag"""


@dataclass
class GroupRequestEvent(RequestEvent):
    """
    加群请求/邀请事件
    """
    sub_type: str = ""
    """
    子类型
    add: 加群请求
    invite: 邀请登录号入群
    """
    
    group_id: int = 0
    """群号"""
    
    user_id: int = 0
    """发送请求的 QQ 号"""
    
    comment: str = ""
    """验证信息"""
    
    flag: str = ""
    """请求 flag，在调用处理请求的 API 时需要传入此 flag"""

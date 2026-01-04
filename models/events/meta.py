"""
元事件模型模块

定义了元事件相关的事件类，包括心跳事件和生命周期事件。
"""
from dataclasses import dataclass, field
from typing import Optional
from .base import OneBotEvent, EventType


@dataclass(slots=True)
class HeartbeatStatus:
    """
    心跳状态接口
    """
    online: Optional[bool] = None  # 是否在线
    good: bool = True  # 状态是否良好


class LifeCycleSubType:
    """
    生命周期子类型枚举
    """
    ENABLE = 'enable'    # 启用
    DISABLE = 'disable'  # 禁用
    CONNECT = 'connect'  # 连接


@dataclass
class MetaEvent(OneBotEvent):
    """
    元事件基类
    """

    meta_event_type: str
    """元事件类型"""

    @property
    def post_type(self) -> str:
        return EventType.META


@dataclass
class HeartbeatEvent(MetaEvent):
    """
    心跳事件，用于确认连接状态
    """
    meta_event_type: str = 'heartbeat'
    """元事件类型：心跳事件"""
    
    status: HeartbeatStatus = field(default_factory=HeartbeatStatus)
    """状态信息"""
    
    interval: int = 0
    """心跳间隔时间(ms)"""


@dataclass
class LifeCycleEvent(MetaEvent):
    """
    生命周期事件，用于通知框架生命周期变化
    """
    meta_event_type: str = 'lifecycle'
    """元事件类型：生命周期事件"""
    
    sub_type: LifeCycleSubType = LifeCycleSubType.ENABLE
    """子类型：启用、禁用、连接"""

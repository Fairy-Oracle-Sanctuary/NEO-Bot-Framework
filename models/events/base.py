"""
基础事件模型模块

该模块定义了所有 OneBot v11 事件模型的基类 `OneBotEvent` 和
事件类型常量 `EventType`。所有具体的事件模型都应继承自 `OneBotEvent`。
"""
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from core.bot import Bot


class EventType:
    """
    OneBot v11 事件类型常量。

    用于标识不同种类的事件上报。
    """
    META = 'meta_event'
    """元事件 (meta_event): 如心跳、生命周期等。"""
    REQUEST = 'request'
    """请求事件 (request): 如加好友请求、加群请求等。"""
    NOTICE = 'notice'
    """通知事件 (notice): 如群成员增加、文件上传等。"""
    MESSAGE = 'message'
    """消息事件 (message): 如私聊消息、群消息等。"""
    MESSAGE_SENT = 'message_sent'
    """消息发送事件 (message_sent): 机器人自己发送消息的上报。"""


@dataclass(slots=True)
class OneBotEvent(ABC):
    """
    OneBot v11 事件的抽象基类。

    所有具体的事件模型都必须继承此类，并实现 `post_type` 属性。

    Attributes:
        time (int): 事件发生的时间戳 (秒)。
        self_id (int): 收到事件的机器人 QQ 号。
        _bot (Optional[Bot]): 内部持有的 Bot 实例引用，用于快捷 API 调用。
    """

    time: int
    self_id: int
    _bot: Optional["Bot"] = field(default=None, init=False)

    @property
    @abstractmethod
    def post_type(self) -> str:
        """
        抽象属性，代表事件的上报类型。

        子类必须重写此属性，并返回对应的 `EventType` 常量值。
        例如: `return EventType.MESSAGE`
        """
        pass

    @property
    def bot(self) -> "Bot":
        """
        获取与此事件关联的 `Bot` 实例，以便快捷调用 API。

        Returns:
            Bot: 当前事件所对应的 `Bot` 实例。

        Raises:
            ValueError: 如果 `Bot` 实例尚未被设置到事件对象中。
        """
        if self._bot is None:
            raise ValueError("Bot instance not set for this event")
        return self._bot

    @bot.setter
    def bot(self, value: "Bot"):
        """
        为事件对象设置关联的 `Bot` 实例。

        Args:
            value (Bot): 要设置的 `Bot` 实例。
        """
        self._bot = value


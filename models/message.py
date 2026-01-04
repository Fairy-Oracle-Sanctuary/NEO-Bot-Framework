"""
消息段模型模块

该模块定义了 `MessageSegment` 类，用于构建和表示 OneBot v11 协议中的消息段。
通过此类，可以方便地创建文本、图片、At 等不同类型的消息内容，并支持链式操作。
"""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(slots=True)
class MessageSegment:
    """
    表示一个 OneBot v11 消息段。

    Attributes:
        type (str): 消息段的类型，例如 'text', 'image', 'at'。
        data (Dict[str, Any]): 消息段的具体数据，是一个键值对字典。
    """

    type: str
    data: Dict[str, Any]

    @property
    def text(self) -> str:
        """
        当消息段类型为 'text' 时，快速获取其文本内容。

        Returns:
            str: 消息段的文本内容。如果类型不是 'text'，则返回空字符串。
        """
        return self.data.get("text", "") if self.type == "text" else ""

    @property
    def image_url(self) -> str:
        """
        当消息段类型为 'image' 时，快速获取其图片 URL。

        Returns:
            str: 图片的 URL。如果类型不是 'image' 或数据中不含 'url'，则返回空字符串。
        """
        return self.data.get("url", "") if self.type == "image" else ""

    def is_at(self, user_id: int = None) -> bool:
        """
        检查当前消息段是否是一个 'at' (提及) 消息段。

        Args:
            user_id (int, optional): 如果提供，则进一步检查被提及的 QQ 号是否匹配。
                                     Defaults to None.

        Returns:
            bool: 如果消息段是 'at' 类型且 user_id 匹配 (如果提供)，则返回 True。
        """
        if self.type != "at":
            return False
        if user_id is None:
            return True
        return str(self.data.get("qq")) == str(user_id)

    def __repr__(self):
        """
        返回消息段对象的字符串表示形式，便于调试。
        """
        return f"[MS:{self.type}:{self.data}]"

    # --- 快捷构造方法 ---

    @staticmethod
    def text(text: str) -> "MessageSegment":  # noqa: F811
        """
        创建一个文本消息段。

        Args:
            text (str): 文本内容。

        Returns:
            MessageSegment: 一个类型为 'text' 的消息段对象。
        """
        return MessageSegment(type="text", data={"text": text})

    @staticmethod
    def at(user_id: int | str) -> "MessageSegment":
        """
        创建一个 @某人 的消息段。

        Args:
            user_id (int | str): 要提及的 QQ 号。若为 "all"，则表示 @全体成员。

        Returns:
            MessageSegment: 一个类型为 'at' 的消息段对象。
        """
        return MessageSegment(type="at", data={"qq": str(user_id)})

    @staticmethod
    def image(file: str) -> "MessageSegment":
        """
        创建一个图片消息段。

        Args:
            file (str): 图片的路径、URL 或 Base64 编码的字符串。

        Returns:
            MessageSegment: 一个类型为 'image' 的消息段对象。
        """
        return MessageSegment(type="image", data={"file": file})

    @staticmethod
    def face(id: int) -> "MessageSegment":
        """
        创建一个 QQ 表情消息段。

        Args:
            id (int): QQ 表情的 ID。

        Returns:
            MessageSegment: 一个类型为 'face' 的消息段对象。
        """
        return MessageSegment(type="face", data={"id": str(id)})


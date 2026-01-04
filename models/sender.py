"""
发送者模型模块

定义了 Sender 类，用于封装 OneBot 11 的发送者信息。
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Sender:
    """
    发送者信息类，对应 OneBot 11 标准中的 sender 字段
    """

    user_id: int
    """发送者 QQ 号"""

    nickname: str
    """昵称"""

    sex: str = "unknown"
    """性别，male 或 female 或 unknown"""

    age: int = 0
    """年龄"""

    # 群聊特有字段
    card: Optional[str] = None
    """群名片／备注"""

    area: Optional[str] = None
    """地区"""

    level: Optional[str] = None
    """成员等级"""

    role: Optional[str] = None
    """角色，owner 或 admin 或 member"""

    title: Optional[str] = None
    """专属头衔"""

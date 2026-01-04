"""
API 响应数据模型模块

定义了 API 返回的数据结构。
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class GroupInfo:
    """
    群信息
    """
    group_id: int = 0
    """群号"""
    
    group_name: str = ""
    """群名称"""
    
    member_count: int = 0
    """成员数"""
    
    max_member_count: int = 0
    """最大成员数"""


@dataclass
class GroupMemberInfo:
    """
    群成员信息
    """
    group_id: int = 0
    """群号"""
    
    user_id: int = 0
    """QQ 号"""
    
    nickname: str = ""
    """昵称"""
    
    card: str = ""
    """群名片/备注"""
    
    sex: str = "unknown"
    """性别, male 或 female 或 unknown"""
    
    age: int = 0
    """年龄"""
    
    area: str = ""
    """地区"""
    
    join_time: int = 0
    """加群时间戳"""
    
    last_sent_time: int = 0
    """最后发言时间戳"""
    
    level: str = ""
    """成员等级"""
    
    role: str = "member"
    """角色, owner 或 admin 或 member"""
    
    unfriendly: bool = False
    """是否不良记录成员"""
    
    title: str = ""
    """专属头衔"""
    
    title_expire_time: int = 0
    """专属头衔过期时间戳"""
    
    card_changeable: bool = False
    """是否允许修改群名片"""


@dataclass
class FriendInfo:
    """
    好友信息
    """
    user_id: int = 0
    """QQ 号"""
    
    nickname: str = ""
    """昵称"""
    
    remark: str = ""
    """备注"""


@dataclass
class StrangerInfo:
    """
    陌生人信息
    """
    user_id: int = 0
    """QQ 号"""
    
    nickname: str = ""
    """昵称"""
    
    sex: str = "unknown"
    """性别, male 或 female 或 unknown"""
    
    age: int = 0
    """年龄"""


@dataclass
class LoginInfo:
    """
    登录号信息
    """
    user_id: int = 0
    """QQ 号"""
    
    nickname: str = ""
    """昵称"""


@dataclass
class VersionInfo:
    """
    版本信息
    """
    app_name: str = ""
    """应用名称"""
    
    app_version: str = ""
    """应用版本"""
    
    protocol_version: str = ""
    """OneBot 标准版本"""


@dataclass
class Status:
    """
    运行状态
    """
    online: bool = False
    """是否在线"""
    
    good: bool = True
    """运行状态是否良好"""


@dataclass
class EssenceMessage:
    """
    精华消息
    """
    sender_id: int = 0
    """发送者 QQ 号"""
    
    sender_nick: str = ""
    """发送者昵称"""
    
    sender_time: int = 0
    """发送时间"""
    
    operator_id: int = 0
    """操作者 QQ 号"""
    
    operator_nick: str = ""
    """操作者昵称"""
    
    operator_time: int = 0
    """操作时间"""
    
    message_id: int = 0
    """消息 ID"""


@dataclass
class CurrentTalkative:
    """
    龙王信息
    """
    user_id: int = 0
    """QQ 号"""
    
    nickname: str = ""
    """昵称"""
    
    avatar: str = ""
    """头像 URL"""
    
    day_count: int = 0
    """持续天数"""


@dataclass
class HonorInfo:
    """
    荣誉信息
    """
    user_id: int = 0
    """QQ 号"""
    
    nickname: str = ""
    """昵称"""
    
    avatar: str = ""
    """头像 URL"""
    
    description: str = ""
    """荣誉描述"""


@dataclass
class GroupHonorInfo:
    """
    群荣誉信息
    """
    group_id: int = 0
    """群号"""
    
    current_talkative: Optional[CurrentTalkative] = None
    """当前龙王"""
    
    talkative_list: List[HonorInfo] = field(default_factory=list)
    """历史龙王"""
    
    performer_list: List[HonorInfo] = field(default_factory=list)
    """群聊之火"""
    
    legend_list: List[HonorInfo] = field(default_factory=list)
    """群聊炽焰"""
    
    strong_newbie_list: List[HonorInfo] = field(default_factory=list)
    """冒尖小春笋"""
    
    emotion_list: List[HonorInfo] = field(default_factory=list)
    """快乐源泉"""

"""
通知事件模型模块

定义了通知相关的事件类，包括好友通知和群组通知等。
"""
from dataclasses import dataclass, field
from .base import OneBotEvent, EventType


@dataclass(slots=True)
class NoticeEvent(OneBotEvent):
    """
    通知事件基类
    """

    notice_type: str
    """通知类型"""

    @property
    def post_type(self) -> str:
        return EventType.NOTICE


@dataclass
class FriendAddNoticeEvent(NoticeEvent):
    """
    好友添加通知
    """
    user_id: int = 0
    """新好友 QQ 号"""


@dataclass
class FriendRecallNoticeEvent(NoticeEvent):
    """
    好友消息撤回通知
    """
    user_id: int = 0
    """消息发送者 QQ 号"""
    
    message_id: int = 0
    """被撤回的消息 ID"""


@dataclass
class GroupNoticeEvent(NoticeEvent):
    """
    群组通知事件基类
    """
    group_id: int = 0
    """群号"""
    
    user_id: int = 0
    """用户 QQ 号"""


@dataclass
class GroupRecallNoticeEvent(GroupNoticeEvent):
    """
    群消息撤回通知
    """
    operator_id: int = 0
    """操作者 QQ 号"""
    
    message_id: int = 0
    """被撤回的消息 ID"""


@dataclass
class GroupIncreaseNoticeEvent(GroupNoticeEvent):
    """
    群成员增加通知
    """
    operator_id: int = 0
    """操作者 QQ 号"""
    
    sub_type: str = ""
    """
    子类型
    approve: 管理员同意入群
    invite: 管理员邀请入群
    """


@dataclass
class GroupDecreaseNoticeEvent(GroupNoticeEvent):
    """
    群成员减少通知
    """
    operator_id: int = 0
    """操作者 QQ 号（如果是主动退群，则和 user_id 相同）"""
    
    sub_type: str = ""
    """
    子类型
    leave: 主动退群
    kick: 成员被踢
    kick_me: 登录号被踢
    disband: 群被解散
    """


@dataclass
class GroupAdminNoticeEvent(GroupNoticeEvent):
    """
    群管理员变动通知
    """
    sub_type: str = ""
    """
    子类型
    set: 设置管理员
    unset: 取消管理员
    """


@dataclass
class GroupBanNoticeEvent(GroupNoticeEvent):
    """
    群禁言通知
    """
    operator_id: int = 0
    """操作者 QQ 号（管理员）"""
    
    duration: int = 0
    """禁言时长(秒)，0 表示解除禁言"""
    
    sub_type: str = ""
    """
    子类型
    ban: 禁言
    lift_ban: 解除禁言
    """


@dataclass
class GroupUploadFile:
    """
    群文件信息
    """
    id: str = ""
    """文件 ID"""
    
    name: str = ""
    """文件名"""
    
    size: int = 0
    """文件大小(Byte)"""
    
    busid: int = 0
    """文件总线 ID"""


@dataclass
class GroupUploadNoticeEvent(GroupNoticeEvent):
    """
    群文件上传通知
    """
    file: GroupUploadFile = field(default_factory=GroupUploadFile)
    """文件信息"""


@dataclass
class NotifyNoticeEvent(NoticeEvent):
    """
    系统通知事件基类 (notify)
    """
    sub_type: str = ""
    """
    子类型
    poke: 戳一戳
    lucky_king: 运气王
    honor: 群荣誉变更
    """
    user_id: int = 0
    """发送者 QQ 号"""


@dataclass
class PokeNotifyEvent(NotifyNoticeEvent):
    """
    戳一戳通知
    """
    target_id: int = 0
    """被戳者 QQ 号"""
    
    group_id: int = 0
    """群号 (如果是群内戳一戳)"""


@dataclass
class LuckyKingNotifyEvent(NotifyNoticeEvent):
    """
    群红包运气王通知
    """
    group_id: int = 0
    """群号"""
    
    target_id: int = 0
    """运气王 QQ 号"""


@dataclass
class HonorNotifyEvent(NotifyNoticeEvent):
    """
    群荣誉变更通知
    """
    group_id: int = 0
    """群号"""
    
    honor_type: str = ""
    """
    荣誉类型
    talkative: 龙王
    performer: 群聊之火
    emotion: 快乐源泉
    """


@dataclass
class GroupCardNoticeEvent(GroupNoticeEvent):
    """
    群成员名片更新通知
    """
    card_new: str = ""
    """新名片"""
    
    card_old: str = ""
    """旧名片"""


@dataclass
class OfflineFile:
    """
    离线文件信息
    """
    name: str = ""
    """文件名"""
    
    size: int = 0
    """文件大小"""
    
    url: str = ""
    """下载链接"""


@dataclass
class OfflineFileNoticeEvent(NoticeEvent):
    """
    接收离线文件通知
    """
    user_id: int = 0
    """发送者 QQ 号"""
    
    file: OfflineFile = field(default_factory=OfflineFile)
    """文件数据"""


@dataclass
class ClientStatus:
    """
    客户端状态
    """
    online: bool = False
    """是否在线"""
    
    status: str = ""
    """状态描述"""


@dataclass
class ClientStatusNoticeEvent(NoticeEvent):
    """
    其他客户端在线状态变更通知
    """
    client: ClientStatus = field(default_factory=ClientStatus)
    """客户端信息"""


@dataclass
class EssenceNoticeEvent(GroupNoticeEvent):
    """
    精华消息变动通知
    """
    sub_type: str = ""
    """
    子类型
    add: 添加
    delete: 删除
    """
    
    sender_id: int = 0
    """消息发送者 ID"""
    
    operator_id: int = 0
    """操作者 ID"""
    
    message_id: int = 0
    """消息 ID"""


"""
事件工厂模块

用于根据 JSON 数据创建对应的事件对象。
"""
from typing import Any, Dict

from models.message import MessageSegment
from models.sender import Sender
from .base import OneBotEvent, EventType
from .message import GroupMessageEvent, PrivateMessageEvent, Anonymous
from .notice import (
    NoticeEvent, FriendAddNoticeEvent, FriendRecallNoticeEvent,
    GroupRecallNoticeEvent, GroupIncreaseNoticeEvent,
    GroupDecreaseNoticeEvent, GroupAdminNoticeEvent, GroupBanNoticeEvent,
    GroupUploadNoticeEvent, GroupUploadFile,
    NotifyNoticeEvent, PokeNotifyEvent, LuckyKingNotifyEvent, HonorNotifyEvent,
    GroupCardNoticeEvent, OfflineFileNoticeEvent, OfflineFile,
    ClientStatusNoticeEvent, ClientStatus, EssenceNoticeEvent
)
from .request import RequestEvent, FriendRequestEvent, GroupRequestEvent
from .meta import MetaEvent, HeartbeatEvent, LifeCycleEvent, HeartbeatStatus


class EventFactory:
    """
    事件工厂类
    """

    @staticmethod
    def create_event(data: Dict[str, Any]) -> OneBotEvent:
        """
        根据数据创建事件对象

        :param data: 事件数据字典
        :return: 对应的事件对象
        :raises ValueError: 如果事件类型未知
        """
        post_type = data.get("post_type")
        
        # 提取公共字段
        common_args = {
            "time": data.get("time", 0),
            "self_id": data.get("self_id", 0),
        }

        if post_type == EventType.MESSAGE or post_type == EventType.MESSAGE_SENT:
            return EventFactory._create_message_event(data, common_args)
        elif post_type == EventType.NOTICE:
            return EventFactory._create_notice_event(data, common_args)
        elif post_type == EventType.REQUEST:
            return EventFactory._create_request_event(data, common_args)
        elif post_type == EventType.META:
            return EventFactory._create_meta_event(data, common_args)
        else:
            # 未知类型的事件，抛出异常
            raise ValueError(f"Unknown event type: {post_type}")

    @staticmethod
    def _create_message_event(data: Dict[str, Any], common_args: Dict[str, Any]) -> OneBotEvent:
        """
        创建消息事件

        :param data: 事件数据
        :param common_args: 公共参数
        :return: 消息事件对象
        """
        message_type = data.get("message_type")
        
        # 解析消息段
        message_list = []
        raw_message_list = data.get("message", [])
        if isinstance(raw_message_list, list):
            for item in raw_message_list:
                if isinstance(item, dict):
                    message_list.append(MessageSegment(type=item.get("type", ""), data=item.get("data", {})))
        
        # 解析发送者
        sender_data = data.get("sender", {})
        sender = Sender(
            user_id=sender_data.get("user_id", 0),
            nickname=sender_data.get("nickname", ""),
            sex=sender_data.get("sex", "unknown"),
            age=sender_data.get("age", 0),
            card=sender_data.get("card"),
            area=sender_data.get("area"),
            level=sender_data.get("level"),
            role=sender_data.get("role"),
            title=sender_data.get("title"),
        )

        msg_args = {
            **common_args,
            "message_type": message_type,
            "sub_type": data.get("sub_type", ""),
            "message_id": data.get("message_id", 0),
            "user_id": data.get("user_id", 0),
            "message": message_list,
            "raw_message": data.get("raw_message", ""),
            "font": data.get("font", 0),
            "sender": sender,
        }

        if message_type == "private":
            return PrivateMessageEvent(**msg_args)
        elif message_type == "group":
            anonymous_data = data.get("anonymous")
            anonymous = None
            if anonymous_data:
                anonymous = Anonymous(
                    id=anonymous_data.get("id", 0),
                    name=anonymous_data.get("name", ""),
                    flag=anonymous_data.get("flag", "")
                )
            return GroupMessageEvent(
                **msg_args,
                group_id=data.get("group_id", 0),
                anonymous=anonymous,
            )
        else:
            # 未知消息类型，抛出异常
            raise ValueError(f"Unknown message type: {message_type}")

    @staticmethod
    def _create_notice_event(data: Dict[str, Any], common_args: Dict[str, Any]) -> OneBotEvent:
        """
        创建通知事件

        :param data: 事件数据
        :param common_args: 公共参数
        :return: 通知事件对象
        """
        notice_type = data.get("notice_type", "")
        
        # 好友相关通知
        if notice_type == "friend_add":
            return FriendAddNoticeEvent(
                **common_args,
                notice_type=notice_type,
                user_id=data.get("user_id", 0)
            )
        elif notice_type == "friend_recall":
            return FriendRecallNoticeEvent(
                **common_args,
                notice_type=notice_type,
                user_id=data.get("user_id", 0),
                message_id=data.get("message_id", 0)
            )
        # 群相关通知
        elif notice_type == "group_recall":
            return GroupRecallNoticeEvent(
                **common_args,
                notice_type=notice_type,
                group_id=data.get("group_id", 0),
                user_id=data.get("user_id", 0),
                operator_id=data.get("operator_id", 0),
                message_id=data.get("message_id", 0)
            )
        elif notice_type == "group_increase":
            return GroupIncreaseNoticeEvent(
                **common_args,
                notice_type=notice_type,
                group_id=data.get("group_id", 0),
                user_id=data.get("user_id", 0),
                operator_id=data.get("operator_id", 0),
                sub_type=data.get("sub_type", "")
            )
        elif notice_type == "group_decrease":
            return GroupDecreaseNoticeEvent(
                **common_args,
                notice_type=notice_type,
                group_id=data.get("group_id", 0),
                user_id=data.get("user_id", 0),
                operator_id=data.get("operator_id", 0),
                sub_type=data.get("sub_type", "")
            )
        elif notice_type == "group_admin":
            return GroupAdminNoticeEvent(
                **common_args,
                notice_type=notice_type,
                group_id=data.get("group_id", 0),
                user_id=data.get("user_id", 0),
                sub_type=data.get("sub_type", "")
            )
        elif notice_type == "group_ban":
            return GroupBanNoticeEvent(
                **common_args,
                notice_type=notice_type,
                group_id=data.get("group_id", 0),
                user_id=data.get("user_id", 0),
                operator_id=data.get("operator_id", 0),
                duration=data.get("duration", 0),
                sub_type=data.get("sub_type", "")
            )
        elif notice_type == "group_upload":
            file_data = data.get("file", {})
            file = GroupUploadFile(
                id=file_data.get("id", ""),
                name=file_data.get("name", ""),
                size=file_data.get("size", 0),
                busid=file_data.get("busid", 0)
            )
            return GroupUploadNoticeEvent(
                **common_args,
                notice_type=notice_type,
                group_id=data.get("group_id", 0),
                user_id=data.get("user_id", 0),
                file=file
            )
        elif notice_type == "notify":
            sub_type = data.get("sub_type", "")
            if sub_type == "poke":
                return PokeNotifyEvent(
                    **common_args,
                    notice_type=notice_type,
                    sub_type=sub_type,
                    user_id=data.get("user_id", 0),
                    target_id=data.get("target_id", 0),
                    group_id=data.get("group_id", 0)
                )
            elif sub_type == "lucky_king":
                return LuckyKingNotifyEvent(
                    **common_args,
                    notice_type=notice_type,
                    sub_type=sub_type,
                    user_id=data.get("user_id", 0),
                    group_id=data.get("group_id", 0),
                    target_id=data.get("target_id", 0)
                )
            elif sub_type == "honor":
                return HonorNotifyEvent(
                    **common_args,
                    notice_type=notice_type,
                    sub_type=sub_type,
                    user_id=data.get("user_id", 0),
                    group_id=data.get("group_id", 0),
                    honor_type=data.get("honor_type", "")
                )
            else:
                return NotifyNoticeEvent(
                    **common_args,
                    notice_type=notice_type,
                    sub_type=sub_type,
                    user_id=data.get("user_id", 0)
                )
        elif notice_type == "group_card":
            return GroupCardNoticeEvent(
                **common_args,
                notice_type=notice_type,
                group_id=data.get("group_id", 0),
                user_id=data.get("user_id", 0),
                card_new=data.get("card_new", ""),
                card_old=data.get("card_old", "")
            )
        elif notice_type == "offline_file":
            file_data = data.get("file", {})
            file = OfflineFile(
                name=file_data.get("name", ""),
                size=file_data.get("size", 0),
                url=file_data.get("url", "")
            )
            return OfflineFileNoticeEvent(
                **common_args,
                notice_type=notice_type,
                user_id=data.get("user_id", 0),
                file=file
            )
        elif notice_type == "client_status":
            client_data = data.get("client", {})
            client = ClientStatus(
                online=client_data.get("online", False),
                status=client_data.get("status", "")
            )
            return ClientStatusNoticeEvent(
                **common_args,
                notice_type=notice_type,
                client=client
            )
        elif notice_type == "essence":
            return EssenceNoticeEvent(
                **common_args,
                notice_type=notice_type,
                sub_type=data.get("sub_type", ""),
                group_id=data.get("group_id", 0),
                sender_id=data.get("sender_id", 0),
                operator_id=data.get("operator_id", 0),
                message_id=data.get("message_id", 0)
            )
        else:
            # 未知通知类型，返回基础通知事件
            return NoticeEvent(**common_args, notice_type=notice_type)

    @staticmethod
    def _create_request_event(data: Dict[str, Any], common_args: Dict[str, Any]) -> OneBotEvent:
        """
        创建请求事件

        :param data: 事件数据
        :param common_args: 公共参数
        :return: 请求事件对象
        """
        request_type = data.get("request_type", "")
        
        if request_type == "friend":
            return FriendRequestEvent(
                **common_args,
                request_type=request_type,
                user_id=data.get("user_id", 0),
                comment=data.get("comment", ""),
                flag=data.get("flag", "")
            )
        elif request_type == "group":
            return GroupRequestEvent(
                **common_args,
                request_type=request_type,
                sub_type=data.get("sub_type", ""),
                group_id=data.get("group_id", 0),
                user_id=data.get("user_id", 0),
                comment=data.get("comment", ""),
                flag=data.get("flag", "")
            )
        else:
            # 未知请求类型，返回基础请求事件
            return RequestEvent(**common_args, request_type=request_type)

    @staticmethod
    def _create_meta_event(data: Dict[str, Any], common_args: Dict[str, Any]) -> OneBotEvent:
        """
        创建元事件

        :param data: 事件数据
        :param common_args: 公共参数
        :return: 元事件对象
        """
        meta_event_type = data.get("meta_event_type", "")
        
        if meta_event_type == "heartbeat":
            status_data = data.get("status", {})
            status = HeartbeatStatus(
                online=status_data.get("online"),
                good=status_data.get("good", True)
            )
            return HeartbeatEvent(
                **common_args,
                meta_event_type=meta_event_type,
                status=status,
                interval=data.get("interval", 0)
            )
        elif meta_event_type == "lifecycle":
            return LifeCycleEvent(
                **common_args,
                meta_event_type=meta_event_type,
                sub_type=data.get("sub_type", "")
            )
        else:
            # 未知元事件类型，返回基础元事件
            return MetaEvent(**common_args, meta_event_type=meta_event_type)

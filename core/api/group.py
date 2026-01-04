"""
群组相关 API 模块

该模块定义了 `GroupAPI` Mixin 类，提供了所有与群组管理、成员操作
等相关的 OneBot v11 API 封装。
"""
from typing import List, Dict, Any, Optional
import json
from core.redis_manager import redis_manager
from .base import BaseAPI
from models.objects import GroupInfo, GroupMemberInfo, GroupHonorInfo


class GroupAPI(BaseAPI):
    """
    `GroupAPI` Mixin 类，提供了所有与群组操作相关的 API 方法。
    """

    async def set_group_kick(self, group_id: int, user_id: int, reject_add_request: bool = False) -> Dict[str, Any]:
        """
        将指定成员踢出群组。

        Args:
            group_id (int): 目标群组的群号。
            user_id (int): 要踢出的成员的 QQ 号。
            reject_add_request (bool, optional): 是否拒绝该用户此后的加群请求。Defaults to False.

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_group_kick", {"group_id": group_id, "user_id": user_id, "reject_add_request": reject_add_request})

    async def set_group_ban(self, group_id: int, user_id: int, duration: int = 1800) -> Dict[str, Any]:
        """
        禁言群组中的指定成员。

        Args:
            group_id (int): 目标群组的群号。
            user_id (int): 要禁言的成员的 QQ 号。
            duration (int, optional): 禁言时长，单位为秒。设置为 0 表示解除禁言。
                                      Defaults to 1800 (30 分钟).

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_group_ban", {"group_id": group_id, "user_id": user_id, "duration": duration})

    async def set_group_anonymous_ban(self, group_id: int, anonymous: Dict[str, Any] = None, duration: int = 1800, flag: str = None) -> Dict[str, Any]:
        """
        禁言群组中的匿名用户。

        Args:
            group_id (int): 目标群组的群号。
            anonymous (Dict[str, Any], optional): 要禁言的匿名用户对象，
                可从群消息事件的 `anonymous` 字段中获取。Defaults to None.
            duration (int, optional): 禁言时长，单位为秒。Defaults to 1800.
            flag (str, optional): 要禁言的匿名用户的 flag 标识，
                可从群消息事件的 `anonymous` 字段中获取。Defaults to None.

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        params = {"group_id": group_id, "duration": duration}
        if anonymous:
            params["anonymous"] = anonymous
        if flag:
            params["flag"] = flag
        return await self.call_api("set_group_anonymous_ban", params)

    async def set_group_whole_ban(self, group_id: int, enable: bool = True) -> Dict[str, Any]:
        """
        开启或关闭群组全员禁言。

        Args:
            group_id (int): 目标群组的群号。
            enable (bool, optional): True 表示开启全员禁言，False 表示关闭。Defaults to True.

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_group_whole_ban", {"group_id": group_id, "enable": enable})

    async def set_group_admin(self, group_id: int, user_id: int, enable: bool = True) -> Dict[str, Any]:
        """
        设置或取消群组成员的管理员权限。

        Args:
            group_id (int): 目标群组的群号。
            user_id (int): 目标成员的 QQ 号。
            enable (bool, optional): True 表示设为管理员，False 表示取消管理员。Defaults to True.

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_group_admin", {"group_id": group_id, "user_id": user_id, "enable": enable})

    async def set_group_anonymous(self, group_id: int, enable: bool = True) -> Dict[str, Any]:
        """
        开启或关闭群组的匿名聊天功能。

        Args:
            group_id (int): 目标群组的群号。
            enable (bool, optional): True 表示开启匿名，False 表示关闭。Defaults to True.

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_group_anonymous", {"group_id": group_id, "enable": enable})

    async def set_group_card(self, group_id: int, user_id: int, card: str = "") -> Dict[str, Any]:
        """
        设置群组成员的群名片。

        Args:
            group_id (int): 目标群组的群号。
            user_id (int): 目标成员的 QQ 号。
            card (str, optional): 要设置的群名片内容。
                传入空字符串 `""` 或 `None` 表示删除该成员的群名片。Defaults to "".

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_group_card", {"group_id": group_id, "user_id": user_id, "card": card})

    async def set_group_name(self, group_id: int, group_name: str) -> Dict[str, Any]:
        """
        设置群组的名称。

        Args:
            group_id (int): 目标群组的群号。
            group_name (str): 新的群组名称。

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_group_name", {"group_id": group_id, "group_name": group_name})

    async def set_group_leave(self, group_id: int, is_dismiss: bool = False) -> Dict[str, Any]:
        """
        退出或解散一个群组。

        Args:
            group_id (int): 目标群组的群号。
            is_dismiss (bool, optional): 是否解散群组。
                仅当机器人是群主时，此项设为 True 才能解散群。Defaults to False.

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_group_leave", {"group_id": group_id, "is_dismiss": is_dismiss})

    async def set_group_special_title(self, group_id: int, user_id: int, special_title: str = "", duration: int = -1) -> Dict[str, Any]:
        """
        为群组成员设置专属头衔。

        Args:
            group_id (int): 目标群组的群号。
            user_id (int): 目标成员的 QQ 号。
            special_title (str, optional): 专属头衔内容。
                传入空字符串 `""` 或 `None` 表示删除头衔。Defaults to "".
            duration (int, optional): 头衔有效期，单位为秒。-1 表示永久。Defaults to -1.

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_group_special_title", {"group_id": group_id, "user_id": user_id, "special_title": special_title, "duration": duration})

    async def get_group_info(self, group_id: int, no_cache: bool = False) -> GroupInfo:
        """
        获取群组的详细信息。

        Args:
            group_id (int): 目标群组的群号。
            no_cache (bool, optional): 是否不使用缓存，直接从服务器获取最新信息。Defaults to False.

        Returns:
            GroupInfo: 包含群组信息的 `GroupInfo` 数据对象。
        """
        cache_key = f"neobot:cache:get_group_info:{group_id}"
        if not no_cache:
            cached_data = await redis_manager.redis.get(cache_key)
            if cached_data:
                return GroupInfo(**json.loads(cached_data))

        res = await self.call_api("get_group_info", {"group_id": group_id})
        await redis_manager.redis.set(cache_key, json.dumps(res), ex=3600)  # 缓存 1 小时
        return GroupInfo(**res)

    async def get_group_list(self) -> List[GroupInfo]:
        """
        获取机器人加入的所有群组的列表。

        Returns:
            List[GroupInfo]: 包含所有群组信息的 `GroupInfo` 对象列表。
        """
        res = await self.call_api("get_group_list")
        return [GroupInfo(**item) for item in res]

    async def get_group_member_info(self, group_id: int, user_id: int, no_cache: bool = False) -> GroupMemberInfo:
        """
        获取指定群组成员的详细信息。

        Args:
            group_id (int): 目标群组的群号。
            user_id (int): 目标成员的 QQ 号。
            no_cache (bool, optional): 是否不使用缓存。Defaults to False.

        Returns:
            GroupMemberInfo: 包含群成员信息的 `GroupMemberInfo` 数据对象。
        """
        cache_key = f"neobot:cache:get_group_member_info:{group_id}:{user_id}"
        if not no_cache:
            cached_data = await redis_manager.redis.get(cache_key)
            if cached_data:
                return GroupMemberInfo(**json.loads(cached_data))

        res = await self.call_api("get_group_member_info", {"group_id": group_id, "user_id": user_id})
        await redis_manager.redis.set(cache_key, json.dumps(res), ex=3600)  # 缓存 1 小时
        return GroupMemberInfo(**res)

    async def get_group_member_list(self, group_id: int) -> List[GroupMemberInfo]:
        """
        获取一个群组的所有成员列表。

        Args:
            group_id (int): 目标群组的群号。

        Returns:
            List[GroupMemberInfo]: 包含所有群成员信息的 `GroupMemberInfo` 对象列表。
        """
        res = await self.call_api("get_group_member_list", {"group_id": group_id})
        return [GroupMemberInfo(**item) for item in res]

    async def get_group_honor_info(self, group_id: int, type: str) -> GroupHonorInfo:
        """
        获取群组的荣誉信息（如龙王、群聊之火等）。

        Args:
            group_id (int): 目标群组的群号。
            type (str): 要获取的荣誉类型。
                可选值: "talkative", "performer", "legend", "strong_newbie", "emotion" 等。

        Returns:
            GroupHonorInfo: 包含群荣誉信息的 `GroupHonorInfo` 数据对象。
        """
        res = await self.call_api("get_group_honor_info", {"group_id": group_id, "type": type})
        return GroupHonorInfo(**res)

    async def set_group_add_request(self, flag: str, sub_type: str, approve: bool = True, reason: str = "") -> Dict[str, Any]:
        """
        处理加群请求或邀请。

        Args:
            flag (str): 请求的标识，需要从 `request` 事件中获取。
            sub_type (str): 请求的子类型，`add` 或 `invite`，
                需要与 `request` 事件中的 `sub_type` 字段相符。
            approve (bool, optional): 是否同意请求或邀请。Defaults to True.
            reason (str, optional): 拒绝加群的理由（仅在 `approve` 为 False 时有效）。Defaults to "".

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_group_add_request", {"flag": flag, "sub_type": sub_type, "approve": approve, "reason": reason})


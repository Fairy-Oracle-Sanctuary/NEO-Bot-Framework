"""
账号与状态相关 API 模块

该模块定义了 `AccountAPI` Mixin 类，提供了所有与机器人自身账号信息、
状态设置等相关的 OneBot v11 API 封装。
"""
import json
from typing import Dict, Any
from .base import BaseAPI
from models.objects import LoginInfo, VersionInfo, Status
from core.redis_manager import redis_manager


class AccountAPI(BaseAPI):
    """
    `AccountAPI` Mixin 类，提供了所有与机器人账号、状态相关的 API 方法。
    """

    async def get_login_info(self, no_cache: bool = False) -> LoginInfo:
        """
        获取当前登录的机器人账号信息。

        Args:
            no_cache (bool, optional): 是否不使用缓存，直接从服务器获取最新信息。Defaults to False.

        Returns:
            LoginInfo: 包含登录号 QQ 和昵称的 `LoginInfo` 数据对象。
        """
        cache_key = f"neobot:cache:get_login_info:{self.self_id}"
        if not no_cache:
            cached_data = await redis_manager.get(cache_key)
            if cached_data:
                return LoginInfo(**json.loads(cached_data))

        res = await self.call_api("get_login_info")
        await redis_manager.set(cache_key, json.dumps(res), ex=3600)  # 缓存 1 小时
        return LoginInfo(**res)

    async def get_version_info(self) -> VersionInfo:
        """
        获取 OneBot v11 实现的版本信息。

        Returns:
            VersionInfo: 包含 OneBot 实现版本信息的 `VersionInfo` 数据对象。
        """
        res = await self.call_api("get_version_info")
        return VersionInfo(**res)

    async def get_status(self) -> Status:
        """
        获取 OneBot v11 实现的状态信息。

        Returns:
            Status: 包含 OneBot 状态信息的 `Status` 数据对象。
        """
        res = await self.call_api("get_status")
        return Status(**res)

    async def bot_exit(self) -> Dict[str, Any]:
        """
        让机器人进程退出（需要实现端支持）。

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("bot_exit")

    async def set_self_longnick(self, long_nick: str) -> Dict[str, Any]:
        """
        设置机器人账号的个性签名。

        Args:
            long_nick (str): 要设置的个性签名内容。

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_self_longnick", {"longNick": long_nick})

    async def set_input_status(self, user_id: int, event_type: int) -> Dict[str, Any]:
        """
        设置 "对方正在输入..." 状态提示。

        Args:
            user_id (int): 目标用户的 QQ 号。
            event_type (int): 事件类型。

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_input_status", {"user_id": user_id, "event_type": event_type})

    async def set_diy_online_status(self, face_id: int, face_type: int, wording: str) -> Dict[str, Any]:
        """
        设置自定义的 "在线状态"。

        Args:
            face_id (int): 状态的表情 ID。
            face_type (int): 状态的表情类型。
            wording (str): 状态的描述文本。

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_diy_online_status", {
            "face_id": face_id,
            "face_type": face_type,
            "wording": wording
        })

    async def set_online_status(self, status_code: int) -> Dict[str, Any]:
        """
        设置在线状态（如在线、离开、摸鱼等）。

        Args:
            status_code (int): 目标在线状态的状态码。

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_online_status", {"status_code": status_code})

    async def set_qq_profile(self, **kwargs) -> Dict[str, Any]:
        """
        设置机器人账号的个人资料。

        Args:
            **kwargs: 个人资料的相关参数，具体字段请参考 OneBot v11 规范。

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_qq_profile", kwargs)

    async def set_qq_avatar(self, **kwargs) -> Dict[str, Any]:
        """
        设置机器人账号的头像。

        Args:
            **kwargs: 头像的相关参数，具体字段请参考 OneBot v11 规范。

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("set_qq_avatar", kwargs)

    async def get_clientkey(self) -> Dict[str, Any]:
        """
        获取客户端密钥（通常用于 QQ 登录相关操作）。

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("get_clientkey")

    async def clean_cache(self) -> Dict[str, Any]:
        """
        清理 OneBot v11 实现端的缓存。

        Returns:
            Dict[str, Any]: OneBot API 的响应数据。
        """
        return await self.call_api("clean_cache")


"""
管理员管理器模块

该模块负责管理机器人的管理员列表。
它实现了文件和 Redis 缓存之间的数据同步，并提供了一套清晰的 API
供其他模块调用。
"""
import json
import os
from typing import Set

from .logger import logger


class AdminManager:
    """
    管理员管理器类

    负责加载、缓存和管理管理员列表。
    使用单例模式，确保全局只有一个实例。
    """
    _instance = None
    _REDIS_KEY = "neobot:admins"  # 用于存储管理员集合的 Redis 键

    def __new__(cls):
        """
        单例模式实现
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        初始化 AdminManager
        """
        if getattr(self, "_initialized", False):
            return

        # 管理员数据文件路径
        self.data_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "data",
            "admin.json"
        )
        
        self._admins: Set[int] = set()
        self._initialized = True
        logger.info("管理员管理器初始化完成")

    async def initialize(self):
        """
        异步初始化，加载数据并同步到 Redis
        """
        await self._load_from_file()
        await self._sync_to_redis()
        logger.info("管理员数据加载并同步到 Redis 完成")

    async def _load_from_file(self):
        """
        从 admin.json 加载管理员列表
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    admins = data.get("admins", [])
                    self._admins = set(int(admin_id) for admin_id in admins)
                    logger.debug(f"从 {self.data_file} 加载了 {len(self._admins)} 位管理员")
            else:
                # 如果文件不存在，创建一个空的
                self._admins = set()
                await self._save_to_file()
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"加载或解析 admin.json 失败: {e}")
            self._admins = set()

    async def _save_to_file(self):
        """
        将当前管理员列表保存回 admin.json
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            # 将 set 转换为 list 以便 JSON 序列化
            admin_list = [str(admin_id) for admin_id in self._admins]
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump({"admins": admin_list}, f, indent=2, ensure_ascii=False)
            logger.debug(f"管理员列表已保存到 {self.data_file}")
        except Exception as e:
            logger.error(f"保存 admin.json 失败: {e}")

    async def _sync_to_redis(self):
        """
        将内存中的管理员集合同步到 Redis
        """
        from .redis_manager import redis_manager
        try:
            # 首先清空旧的集合
            await redis_manager.redis.delete(self._REDIS_KEY)
            if self._admins:
                # 将所有管理员ID添加到集合中
                await redis_manager.redis.sadd(self._REDIS_KEY, *self._admins)
            logger.debug(f"已将 {len(self._admins)} 位管理员同步到 Redis")
        except Exception as e:
            logger.error(f"同步管理员到 Redis 失败: {e}")

    async def is_admin(self, user_id: int) -> bool:
        """
        检查用户是否为管理员（从 Redis 缓存读取）
        """
        from .redis_manager import redis_manager
        try:
            return await redis_manager.redis.sismember(self._REDIS_KEY, user_id)
        except Exception as e:
            logger.error(f"从 Redis 检查管理员权限失败: {e}")
            # Redis 失败时，回退到内存检查
            return user_id in self._admins

    async def add_admin(self, user_id: int) -> bool:
        """
        添加管理员，并同步到文件和 Redis
        """
        from .redis_manager import redis_manager
        if user_id in self._admins:
            return False  # 用户已经是管理员

        self._admins.add(user_id)
        await self._save_to_file()
        try:
            await redis_manager.redis.sadd(self._REDIS_KEY, user_id)
            logger.info(f"已添加新管理员 {user_id} 并更新缓存")
            return True
        except Exception as e:
            logger.error(f"添加管理员 {user_id} 到 Redis 失败: {e}")
            return False

    async def remove_admin(self, user_id: int) -> bool:
        """
        移除管理员，并同步到文件和 Redis
        """
        from .redis_manager import redis_manager
        if user_id not in self._admins:
            return False  # 用户不是管理员

        self._admins.remove(user_id)
        await self._save_to_file()
        try:
            await redis_manager.redis.srem(self._REDIS_KEY, user_id)
            logger.info(f"已移除管理员 {user_id} 并更新缓存")
            return True
        except Exception as e:
            logger.error(f"从 Redis 移除管理员 {user_id} 失败: {e}")
            return False

    async def get_all_admins(self) -> Set[int]:
        """
        获取所有管理员的集合
        """
        return self._admins.copy()


# 全局 AdminManager 实例
admin_manager = AdminManager()

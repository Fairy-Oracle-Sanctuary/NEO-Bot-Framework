"""
权限管理器模块

该模块负责管理用户权限，支持 admin、op、user 三个权限级别。
权限数据存储在 `permissions.json` 文件中，格式为：
{
    "users": {
        "123456": "admin",
        "789012": "op",
        "345678": "user"
    }
}
"""
import json
import os
from functools import total_ordering
from typing import Dict

from .logger import logger
from .admin_manager import admin_manager  # 导入 AdminManager


@total_ordering
class Permission:
    """
    权限封装类

    封装了权限的名称和等级，并提供了比较方法。
    使用 @total_ordering 装饰器可以自动生成所有的比较运算符。
    """
    def __init__(self, name: str, level: int):
        """
        初始化权限对象

        Args:
            name (str): 权限名称 (e.g., "admin", "op")
            level (int): 权限等级，数字越大权限越高
        """
        self.name = name
        self.level = level

    def __eq__(self, other):
        """
        判断权限是否相等
        """
        if not isinstance(other, Permission):
            return NotImplemented
        return self.level == other.level

    def __lt__(self, other):
        """
        判断权限是否小于另一个权限
        """
        if not isinstance(other, Permission):
            return NotImplemented
        return self.level < other.level

    def __str__(self) -> str:
        """
        返回权限的字符串表示（即权限名称）
        """
        return self.name


# 定义全局权限常量
ADMIN = Permission("admin", 3)
OP = Permission("op", 2)
USER = Permission("user", 1)

# 用于从字符串名称查找权限对象的字典
_PERMISSIONS: Dict[str, Permission] = {
    p.name: p for p in [ADMIN, OP, USER]
}


class PermissionManager:
    """
    权限管理器类

    负责加载、保存和查询用户权限数据。
    使用单例模式，确保全局只有一个权限管理器实例。
    """

    _instance = None

    def __new__(cls):
        """
        单例模式实现

        Returns:
            PermissionManager: 全局唯一的权限管理器实例
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        初始化权限管理器

        如果已经初始化过，则直接返回。
        """
        if getattr(self, "_initialized", False):
            return

        # 权限数据文件路径
        self.data_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "data",
            "permissions.json"
        )

        # 确保数据目录存在
        data_dir = os.path.dirname(self.data_file)
        os.makedirs(data_dir, exist_ok=True)

        # 权限数据存储结构：{"users": {"user_id": "level_name"}}
        self._data: Dict[str, Dict[str, str]] = {"users": {}}

        # 加载现有数据
        self.load()

        self._initialized = True
        logger.info("权限管理器初始化完成")

    def load(self) -> None:
        """
        从文件加载权限数据

        如果文件不存在，则创建空文件并初始化默认数据结构。
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 兼容旧格式
                    if "users" in data:
                        self._data["users"] = data["users"]
                    else:
                        self._data["users"] = {}
                logger.debug(f"权限数据已从 {self.data_file} 加载")
            else:
                # 文件不存在，创建空文件
                self.save()
                logger.debug(f"创建空的权限数据文件: {self.data_file}")
        except json.JSONDecodeError as e:
            logger.error(f"权限数据文件格式错误: {e}")
            # 文件损坏，重置为空数据
            self._data["users"] = {}
            self.save()
        except Exception as e:
            logger.error(f"加载权限数据失败: {e}")
            self._data["users"] = {}

    def save(self) -> None:
        """
        将权限数据保存到文件
        """
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            logger.debug(f"权限数据已保存到 {self.data_file}")
        except Exception as e:
            logger.error(f"保存权限数据失败: {e}")

    async def get_user_permission(self, user_id: int) -> Permission:
        """
        获取指定用户的权限对象

        Args:
            user_id (int): 用户 QQ 号

        Returns:
            Permission: 用户的权限对象，如果用户不存在则返回默认级别 USER
        """
        # 首先，通过 AdminManager 检查是否为管理员
        if await admin_manager.is_admin(user_id):
            return ADMIN

        # 如果不是管理员，则从 permissions.json 中查找
        user_id_str = str(user_id)
        level_name = self._data["users"].get(user_id_str, USER.name)
        return _PERMISSIONS.get(level_name, USER)

    def set_user_permission(self, user_id: int, permission: Permission) -> None:
        """
        设置指定用户的权限级别

        Args:
            user_id (int): 用户 QQ 号
            permission (Permission): 权限对象

        Raises:
            ValueError: 如果权限对象无效
        """
        if not isinstance(permission, Permission) or permission.name not in _PERMISSIONS:
            raise ValueError(f"无效的权限对象: {permission}")

        user_id_str = str(user_id)
        self._data["users"][user_id_str] = permission.name
        self.save()
        logger.info(f"设置用户 {user_id} 的权限级别为 {permission.name}")

    def remove_user(self, user_id: int) -> None:
        """
        移除指定用户的权限设置，恢复为默认级别

        Args:
            user_id (int): 用户 QQ 号
        """
        user_id_str = str(user_id)
        if user_id_str in self._data["users"]:
            del self._data["users"][user_id_str]
            self.save()
            logger.info(f"移除用户 {user_id} 的权限设置")

    async def check_permission(self, user_id: int, required_permission: Permission) -> bool:
        """
        检查用户是否具有指定权限级别

        Args:
            user_id (int): 用户 QQ 号
            required_permission (Permission): 所需的权限对象

        Returns:
            bool: 如果用户权限 >= 所需权限，返回 True，否则返回 False
        """
        user_permission = await self.get_user_permission(user_id)
        return user_permission >= required_permission

    def get_all_users(self) -> Dict[str, str]:
        """
        获取所有设置了权限的用户及其级别名称

        Returns:
            Dict[str, str]: 用户ID到权限级别名称的映射
        """
        return self._data["users"].copy()

    def clear_all(self) -> None:
        """
        清空所有权限设置
        """
        self._data["users"].clear()
        self.save()
        logger.info("已清空所有权限设置")


# 全局权限管理器实例
permission_manager = PermissionManager()
"""
插件管理器模块

负责扫描、加载和管理 `base_plugins` 目录下的所有插件。
"""

import importlib
import json
import os
import pkgutil
import sys

from core.command_manager import matcher
from core.exceptions import SyncHandlerError
from .logger import logger
from .executor import run_in_thread_pool


def load_all_plugins():
    """
    扫描并加载 `plugins` 目录下的所有插件。

    该函数会遍历 `plugins` 目录下的所有模块：
    1. 如果模块已加载，则执行 reload 操作（用于热重载）。
    2. 如果模块未加载，则执行 import 操作。

    加载过程中会提取插件元数据 `__plugin_meta__` 并注册到 CommandManager。
    """
    plugin_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "plugins"
    )
    package_name = "plugins"

    logger.info(f"正在从 {package_name} 加载插件...")

    for loader, module_name, is_pkg in pkgutil.iter_modules([plugin_dir]):
        full_module_name = f"{package_name}.{module_name}"

        try:
            if full_module_name in sys.modules:
                module = importlib.reload(sys.modules[full_module_name])
                action = "重载"
            else:
                module = importlib.import_module(full_module_name)
                action = "加载"

            # 提取插件元数据
            if hasattr(module, "__plugin_meta__"):
                meta = getattr(module, "__plugin_meta__")
                matcher.plugins[full_module_name] = meta

            type_str = "包" if is_pkg else "文件"
            logger.success(f"   [{type_str}] 成功{action}: {module_name}")
        except SyncHandlerError as e:
            logger.error(f"   插件 {module_name} 加载失败: {e} (跳过此插件)")
        except Exception as e:
            print(
                f"   {action if 'action' in locals() else '加载'}插件 {module_name} 失败: {e}"
            )


class PluginDataManager:
    """
    用于管理插件产生的数据文件的类
    """

    def __init__(self, plugin_name: str):
        """
        初始化插件数据管理器

        :param plugin_name: 插件名称
        """
        self.plugin_name = plugin_name
        self.data_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "plugins",
            "data",
            self.plugin_name + ".json",
        )
        self.data = {}

    async def load(self):
        """读取配置文件"""
        if not os.path.exists(self.data_file):
            await self.set(self.plugin_name, [])
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                self.data = await run_in_thread_pool(json.load, f)
        except json.JSONDecodeError:
            self.data = {}

    async def save(self):
        """保存配置到文件"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            await run_in_thread_pool(json.dump, self.data, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        """获取配置项"""
        return self.data.get(key, default)

    async def set(self, key, value):
        """设置配置项"""
        self.data[key] = value
        await self.save()

    async def add(self, key, value):
        """添加配置项"""
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)
        await self.save()

    async def remove(self, key):
        """删除配置项"""
        if key in self.data:
            del self.data[key]
            await self.save()

    async def clear(self):
        """清空所有配置"""
        self.data.clear()
        await self.save()

    def get_all(self):
        return self.data.copy()

"""
配置加载模块

负责读取和解析 config.toml 配置文件，提供全局配置对象。
"""
from pathlib import Path
from typing import Any, Dict

import tomllib


class Config:
    """
    配置加载类，负责读取和解析 config.toml 文件
    """

    def __init__(self, file_path: str = "config.toml"):
        """
        初始化配置加载器

        :param file_path: 配置文件路径，默认为 "config.toml"
        """
        self.path = Path(file_path)
        self._data: Dict[str, Any] = {}
        self.load()

    def load(self):
        """
        加载配置文件

        :raises FileNotFoundError: 如果配置文件不存在
        """
        if not self.path.exists():
            raise FileNotFoundError(f"配置文件 {self.path} 未找到！")

        with open(self.path, "rb") as f:
            self._data = tomllib.load(f)

    # 通过属性访问配置
    @property
    def napcat_ws(self) -> dict:
        """
        获取 NapCat WebSocket 配置

        :return: 配置字典
        """
        return self._data.get("napcat_ws", {})

    @property
    def bot(self) -> dict:
        """
        获取 Bot 基础配置

        :return: 配置字典
        """
        return self._data.get("bot", {})

    @property
    def features(self) -> dict:
        """
        获取功能特性配置

        :return: 配置字典
        """
        return self._data.get("features", {})

    @property
    def redis(self) -> dict:
        """
        获取 Redis 配置

        :return: 配置字典
        """
        return self._data.get("redis", {})


# 实例化全局配置对象
global_config = Config()

if __name__ == "__main__":
    print(global_config.napcat_ws)
    print(global_config.bot.get("command"))
    print(type(global_config.bot.get("command")) is list)
    print(global_config.features)

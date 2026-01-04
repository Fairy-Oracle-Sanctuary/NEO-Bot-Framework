"""
API 基础模块

定义了 API 调用的基础接口。
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseAPI(ABC):
    """
    API 基础抽象类
    """

    @abstractmethod
    async def call_api(self, action: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        调用 API

        :param action: API 动作名称
        :param params: API 参数
        :return: API 响应结果
        """
        raise NotImplementedError

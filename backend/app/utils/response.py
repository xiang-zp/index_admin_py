# -*- coding: utf-8 -*-
"""
API响应工具模块

提供标准化的API响应格式，统一前端处理逻辑。
"""

from typing import Any, Optional


class APIResponse:
    """
    API响应工具类

    提供成功和错误响应的统一格式方法。
    """

    @staticmethod
    def success(data: Any = None, message: str = "success", code: int = 200) -> dict:
        """
        成功响应

        Args:
            data: 响应数据
            message: 响应消息
            code: 响应状态码

        Returns:
            dict: 标准成功响应格式
        """
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @staticmethod
    def error(message: str = "error", code: int = 400, data: Any = None) -> dict:
        """
        错误响应

        Args:
            message: 错误消息
            code: 错误状态码
            data: 附加数据

        Returns:
            dict: 标准错误响应格式
        """
        return {
            "code": code,
            "message": message,
            "data": data
        }

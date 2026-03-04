# -*- coding: utf-8 -*-
"""
应用配置模块

提供应用程序的全局配置管理，支持从 .env 文件读取环境变量。
使用 pydantic-settings 进行配置管理，支持配置验证和类型转换。
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    应用配置类

    包含数据库配置、应用环境配置、CORS配置、LLM配置和JWT配置等。
    所有配置项均可通过环境变量覆盖。
    """

    # 数据库连接配置
    # 格式: mysql+pymysql://username:password@host:port/database_name
    DATABASE_URL: str = "mysql+pymysql://root:1q2w3e4r@127.0.0.1:3306/smart_qa"

    # 应用环境配置
    # 可选值: development, production, testing
    APP_ENV: str = "development"

    # 日志级别配置
    # 可选值: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_LEVEL: str = "INFO"

    # CORS跨域配置
    # 多个域名用逗号分隔
    CORS_ORIGINS: str = "http://localhost:5175,http://127.0.0.1:5175,http://192.168.1.2:5175"

    # LLM API 配置
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "doubao"

    # JWT认证配置
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    @property
    def cors_origins_list(self) -> List[str]:
        """
        将CORS Origins字符串转换为列表

        Returns:
            List[str]: CORS允许的 origins 列表
        """
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        """
        Pydantic 配置类

        - env_file: 指定环境变量文件
        - case_sensitive: 配置键是否区分大小写
        - extra: 忽略额外的配置字段
        """
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# 创建全局配置实例
settings = Settings()

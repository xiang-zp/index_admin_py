# -*- coding: utf-8 -*-
"""
数据库连接模块

提供数据库引擎创建、Session管理和基础模型类。
使用 SQLAlchemy ORM 框架进行数据库操作。
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


# 创建数据库引擎（优化连接池配置）
# 参数说明:
# - echo: 是否输出SQL语句，开发环境为True便于调试
# - pool_size: 连接池大小，默认10个连接
# - max_overflow: 允许超过pool_size的最大连接数
# - pool_recycle: 连接回收时间（秒），避免MySQL连接超时
# - pool_pre_ping: 每次获取连接前先检查连接是否有效
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.APP_ENV == "development",
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)


# 创建 Session 类
# 参数说明:
# - autocommit: 是否自动提交事务，False需要手动commit
# - autoflush: 是否自动刷新缓存，False需要手动flush
# - bind: 绑定的数据库引擎
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 创建 Base 类
# 所有ORM模型类都需要继承此类
Base = declarative_base()


def get_db():
    """
    数据库依赖注入函数

    用于FastAPI的Depends机制，自动获取和释放数据库连接。
    在请求结束后自动关闭连接，避免连接泄漏。

    Yields:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

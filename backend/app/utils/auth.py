# -*- coding: utf-8 -*-
"""
认证工具模块

提供密码哈希、JWT令牌创建和解码等认证相关工具函数。
使用 bcrypt 进行密码加密，python-jose 进行JWT操作。
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确

    Args:
        plain_password: 明文密码
        hashed_password: 加密后的密码

    Returns:
        bool: 密码是否匹配
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """
    生成密码哈希

    使用 bcrypt 算法对密码进行哈希处理。
    每次调用都会生成不同的盐值，确保安全性。

    Args:
        password: 明文密码

    Returns:
        str: 加密后的密码哈希值
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌

    将用户数据编码为JWT令牌，包含过期时间信息。

    Args:
        data: 要编码的数据字典，通常包含用户ID (sub字段)
        expires_delta: 令牌过期时间增量，默认为配置中的JWT_EXPIRATION_HOURS

    Returns:
        str: JWT令牌字符串
    """
    to_encode = data.copy()

    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

    # 添加过期时间到负载
    to_encode.update({"exp": expire})

    # 编码JWT
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    解码JWT访问令牌

    验证并解码JWT令牌，提取用户数据。

    Args:
        token: JWT令牌字符串

    Returns:
        Optional[dict]: 解码后的数据字典，如果令牌无效则返回None
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

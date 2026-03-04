# -*- coding: utf-8 -*-
"""
认证依赖模块

提供用户认证相关的依赖注入函数。
使用 JWT Bearer Token 进行用户身份验证。
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import AdminUser
from app.utils.auth import decode_access_token
from app.utils.logger import get_logger


logger = get_logger(__name__)

# Bearer Token 安全策略
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> AdminUser:
    """
    获取当前登录用户

    从 JWT Token 中解析用户信息，验证用户身份。
    每次请求都会查询数据库获取最新用户信息，确保数据实时性。

    Args:
        credentials: HTTP Bearer Token 凭证
        db: 数据库会话对象

    Returns:
        AdminUser: 当前登录的用户对象

    Raises:
        HTTPException: Token无效或用户不存在时抛出401异常
    """
    # 从Token中获取令牌
    token = credentials.credentials

    # 解码Token
    payload = decode_access_token(token)

    # 验证Token是否有效
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 从Token负载中获取用户ID
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 从数据库查询用户信息
    # 注意：每次都从数据库获取，确保获取最新会话中的用户对象
    # 避免出现 Instance <AdminUser> is not bound to a Session 错误
    user = db.query(AdminUser).filter(AdminUser.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

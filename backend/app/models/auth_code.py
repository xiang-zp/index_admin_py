from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class AuthCode(Base):
    """授权码表"""
    __tablename__ = "auth_codes"
    
    id = Column(String(32), primary_key=True, comment="授权码唯一标识ID")
    description = Column(String(200), nullable=True, comment="授权码描述信息")
    invite_code = Column(String(20), unique=True, nullable=False, index=True, comment="邀请码，用于用户注册")
    status = Column(String(20), default="authorized", nullable=False, index=True, comment="授权状态，如authorized、expired等")
    auth_location = Column(String(20), default="global", nullable=False, comment="授权位置，如global、specific等")
    authorized_user = Column(String(50), nullable=True, comment="已授权的用户名")
    authorized_at = Column(DateTime, nullable=True, comment="授权时间")
    expire_time = Column(DateTime, nullable=True, comment="过期时间")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

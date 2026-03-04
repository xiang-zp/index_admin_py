from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class AdminUser(Base):
    """管理员用户表"""
    __tablename__ = "admin_users"
    
    id = Column(String(32), primary_key=True, comment="用户唯一标识ID")
    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名，用于登录")
    password = Column(String(255), nullable=False, comment="密码，加密存储")
    role = Column(String(20), default="admin", nullable=False, comment="用户角色，如admin、editor等")
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

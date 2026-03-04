from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class AuthLocation(Base):
    __tablename__ = "auth_locations"

    id = Column(String(50), primary_key=True, index=True, comment="授权位置唯一标识ID")
    value = Column(String(100), unique=True, nullable=False, index=True, comment="授权位置值，用于系统识别")
    label = Column(String(100), nullable=False, comment="授权位置标签，用于前端显示")
    description = Column(String(255), nullable=True, comment="授权位置描述信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

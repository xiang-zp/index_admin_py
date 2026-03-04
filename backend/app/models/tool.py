from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Index
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql import func
from app.database import Base


class Tool(Base):
    """开源项目表"""
    __tablename__ = "tools"
    __table_args__ = (
        Index('idx_sort_order', 'sort_order'),
    )
    
    id = Column(String(32), primary_key=True, comment="项目唯一标识ID")
    name = Column(String(100), nullable=False, comment="项目名称")
    title = Column(String(100), nullable=True, comment="项目标题")
    description = Column(Text, nullable=False, comment="项目描述信息")
    path = Column(String(200), nullable=True, comment="项目路径/链接")
    icon = Column(String(50), nullable=True, comment="图标名称")
    image = Column(LONGTEXT, nullable=True, comment="项目图片，支持Base64或URL格式")
    row = Column("row", String(20), nullable=True, default='row1', comment="展示位：row1-第一行，row2-第二行")
    is_visible = Column(Boolean, default=True, nullable=False, index=True, comment="是否在前端显示")
    is_active = Column(Boolean, default=True, nullable=False, index=True, comment="是否激活")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序顺序，数字越小越靠前")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

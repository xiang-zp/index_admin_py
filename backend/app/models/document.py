from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.sql import func
from app.database import Base


class Document(Base):
    """文档资料表"""
    __tablename__ = "documents"
    
    id = Column(String(32), primary_key=True, comment="文档唯一标识ID")
    category = Column(String(50), nullable=False, index=True, comment="文档分类，如技术文档、用户手册等")
    title = Column(String(200), nullable=False, comment="文档标题")
    description = Column(Text, nullable=False, comment="文档描述信息")
    color = Column(String(20), nullable=False, default="#3b82f6", comment="文档显示颜色，十六进制格式")
    url = Column(String(500), nullable=True, comment="文档跳转地址")
    row = Column(String(10), default="row1", nullable=False, comment="展示位：row1第一行，row2第二行")
    is_visible = Column(Boolean, default=True, nullable=False, index=True, comment="是否在前端显示")
    is_active = Column(Boolean, default=True, nullable=False, index=True, comment="是否激活")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序顺序，数字越小越靠前")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

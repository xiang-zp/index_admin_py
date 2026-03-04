from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.sql import func
from app.database import Base


class FooterConfig(Base):
    """底部配置表"""
    __tablename__ = "footer_config"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="配置ID，自增主键")
    logo_url = Column(Text, nullable=True, comment="Logo图片URL地址或Base64图片数据")
    slogan = Column(Text, nullable=True, comment="底部标语或口号")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")


class FooterLink(Base):
    """底部链接表"""
    __tablename__ = "footer_links"
    
    id = Column(String(32), primary_key=True, comment="链接唯一标识ID")
    title = Column(String(100), nullable=False, comment="链接标题")
    url = Column(String(500), nullable=False, comment="链接URL地址")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序顺序，数字越小越靠前")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

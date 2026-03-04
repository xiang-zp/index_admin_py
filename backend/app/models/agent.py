from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.sql import func
from app.database import Base


class Agent(Base):
    """智能体表"""
    __tablename__ = "agents"
    
    id = Column(String(32), primary_key=True, comment="智能体唯一标识ID")
    name = Column(String(100), nullable=False, comment="智能体名称")
    description = Column(Text, nullable=True, comment="智能体描述")
    api = Column(String(500), nullable=False, comment="API接口地址")
    source = Column(String(20), nullable=False, default="内置", comment="来源类型，如内置、自定义等")
    bot_id = Column(String(100), nullable=True, comment="机器人ID，用于第三方平台集成")
    is_visible = Column(Boolean, default=True, nullable=False, index=True, comment="是否在前端显示")
    is_active = Column(Boolean, default=True, nullable=False, index=True, comment="是否激活")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序顺序，数字越小越靠前")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

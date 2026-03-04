from pydantic import BaseModel
from typing import List, Optional


class Project(BaseModel):
    """项目"""
    id: int
    category: str
    title: str
    description: str
    date: str
    color: str


class ProjectListResponse(BaseModel):
    """项目列表响应"""
    total: int
    page: int
    page_size: int
    items: List[Project]


class Category(BaseModel):
    """分类"""
    id: str
    name: str

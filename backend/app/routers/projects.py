from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.project import Project
from app.schemas.project import Project as ProjectSchema, ProjectListResponse, Category
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from typing import Optional

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=dict)
async def get_projects(
    category: Optional[str] = Query(None, description="项目分类"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取项目列表
    """
    try:
        query = db.query(Project).filter(Project.is_active == True)
        
        # 分类筛选
        if category:
            query = query.filter(Project.category == category)
        
        # 获取总数
        total = query.count()
        
        # 分页查询
        items = query.order_by(Project.date.desc()).offset(
            (page - 1) * page_size
        ).limit(page_size).all()
        
        project_list = [
            ProjectSchema(
                id=project.id,
                category=project.category,
                title=project.title,
                description=project.description,
                date=project.date.strftime("%Y-%m-%d"),
                color=project.color
            )
            for project in items
        ]
        
        return APIResponse.success(
            data=ProjectListResponse(
                total=total,
                page=page,
                page_size=page_size,
                items=project_list
            )
        )
        
    except Exception as e:
        logger.error(f"Error getting projects: {e}")
        return APIResponse.error(f"获取项目列表失败: {str(e)}", 500)


@router.get("/categories", response_model=dict)
async def get_project_categories(db: Session = Depends(get_db)):
    """
    获取项目分类
    """
    try:
        # 使用 DISTINCT 获取所有分类
        categories = db.query(Project.category).filter(
            Project.is_active == True
        ).distinct().all()
        
        category_list = [
            Category(
                id=str(i),
                name=category[0]
            )
            for i, category in enumerate(categories)
        ]
        
        return APIResponse.success(data=category_list)
        
    except Exception as e:
        logger.error(f"Error getting project categories: {e}")
        return APIResponse.error(f"获取项目分类失败: {str(e)}", 500)

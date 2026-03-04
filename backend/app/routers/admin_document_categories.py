from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document_category import DocumentCategory
from app.schemas.document import CategoryCreate, CategoryUpdate, CategoryResponseFull
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.dependencies import get_current_user
from app.models.user import AdminUser

router = APIRouter()
logger = get_logger(__name__)

DEFAULT_CATEGORIES = [
    {"name": "python编程", "color": "#3b82f6"},
    {"name": "python自动化", "color": "#10b981"},
    {"name": "测试工具", "color": "#f59e0b"},
    {"name": "测试基础", "color": "#ef4444"},
    {"name": "测试开发", "color": "#8b5cf6"},
]

def init_default_categories(db: Session):
    """初始化默认分类标签"""
    existing_count = db.query(DocumentCategory).count()
    if existing_count == 0:
        for idx, cat in enumerate(DEFAULT_CATEGORIES):
            category = DocumentCategory(
                name=cat["name"],
                color=cat["color"],
                sort_order=idx
            )
            db.add(category)
        db.commit()
        logger.info("Default document categories initialized")


@router.get("", response_model=dict)
async def get_categories(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        init_default_categories(db)
        
        categories = db.query(DocumentCategory).filter(
            DocumentCategory.is_active == True
        ).order_by(DocumentCategory.sort_order).all()
        
        result = [
            {
                "id": cat.id,
                "name": cat.name,
                "color": cat.color,
                "is_active": cat.is_active,
                "sort_order": cat.sort_order,
                "created_at": cat.created_at.isoformat() if cat.created_at else None,
                "updated_at": cat.updated_at.isoformat() if cat.updated_at else None
            }
            for cat in categories
        ]
        return APIResponse.success(data=result)
    except Exception as e:
        logger.error(f"Get categories error: {e}")
        return APIResponse.error(f"获取分类列表失败: {str(e)}", 500)


@router.post("", response_model=dict)
async def create_category(
    request: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        existing = db.query(DocumentCategory).filter(
            DocumentCategory.name == request.name
        ).first()
        if existing:
            return APIResponse.error("分类名称已存在", 400)
        
        max_order = db.query(DocumentCategory).count()
        category = DocumentCategory(
            name=request.name,
            color=request.color,
            sort_order=max_order
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        
        logger.info(f"Category created: {category.id}")
        return APIResponse.success(data={
            "id": category.id,
            "name": category.name,
            "color": category.color,
            "is_active": category.is_active,
            "sort_order": category.sort_order,
            "created_at": category.created_at.isoformat() if category.created_at else None,
            "updated_at": category.updated_at.isoformat() if category.updated_at else None
        })
    except Exception as e:
        logger.error(f"Create category error: {e}")
        db.rollback()
        return APIResponse.error(f"创建分类失败: {str(e)}", 500)


@router.put("/{category_id}", response_model=dict)
async def update_category(
    category_id: int,
    request: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        category = db.query(DocumentCategory).filter(
            DocumentCategory.id == category_id
        ).first()
        if not category:
            return APIResponse.error("分类不存在", 404)
        
        if request.name is not None:
            existing = db.query(DocumentCategory).filter(
                DocumentCategory.name == request.name,
                DocumentCategory.id != category_id
            ).first()
            if existing:
                return APIResponse.error("分类名称已存在", 400)
            category.name = request.name
        
        if request.color is not None:
            category.color = request.color
        
        if request.is_active is not None:
            category.is_active = request.is_active
        
        db.commit()
        db.refresh(category)
        
        logger.info(f"Category updated: {category_id}")
        return APIResponse.success(data={
            "id": category.id,
            "name": category.name,
            "color": category.color,
            "is_active": category.is_active,
            "sort_order": category.sort_order,
            "created_at": category.created_at.isoformat() if category.created_at else None,
            "updated_at": category.updated_at.isoformat() if category.updated_at else None
        })
    except Exception as e:
        logger.error(f"Update category error: {e}")
        db.rollback()
        return APIResponse.error(f"更新分类失败: {str(e)}", 500)


@router.delete("/{category_id}", response_model=dict)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        category = db.query(DocumentCategory).filter(
            DocumentCategory.id == category_id
        ).first()
        if not category:
            return APIResponse.error("分类不存在", 404)
        
        db.delete(category)
        db.commit()
        
        logger.info(f"Category deleted: {category_id}")
        return APIResponse.success(message="删除成功")
    except Exception as e:
        logger.error(f"Delete category error: {e}")
        db.rollback()
        return APIResponse.error(f"删除分类失败: {str(e)}", 500)

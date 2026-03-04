from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document
from app.models.document_category import DocumentCategory
from app.schemas.document import DocumentResponse, DocumentListResponse, CategoryResponse
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from typing import Optional

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=dict)
async def get_documents(
    category: Optional[str] = Query(None, description="文档分类"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取文档列表
    """
    try:
        query = db.query(Document).filter(Document.is_active == True, Document.is_visible == True)
        
        # 分类筛选
        if category and category != 'all':
            query = query.filter(Document.category == category)
        
        # 获取总数
        total = query.count()
        
        # 分页查询
        items = query.order_by(Document.sort_order).offset(
            (page - 1) * page_size
        ).limit(page_size).all()
        
        document_list = [
            DocumentResponse(
                id=document.id,
                category=document.category,
                title=document.title,
                description=document.description,
                color=document.color,
                url=document.url,
                row=document.row,
                is_visible=document.is_visible,
                sort_order=document.sort_order
            )
            for document in items
        ]
        
        return APIResponse.success(
            data=DocumentListResponse(
                items=document_list,
                total=total
            )
        )
        
    except Exception as e:
        logger.error(f"Error getting documents: {e}")
        return APIResponse.error(f"获取文档列表失败: {str(e)}", 500)


@router.get("/categories", response_model=dict)
async def get_document_categories(db: Session = Depends(get_db)):
    """
    获取文档分类（从document_categories表获取）
    """
    try:
        categories = db.query(DocumentCategory).filter(
            DocumentCategory.is_active == True
        ).order_by(DocumentCategory.sort_order).all()
        
        category_list = [
            CategoryResponse(
                id=str(cat.id),
                name=cat.name,
                color=cat.color
            )
            for cat in categories
        ]
        
        return APIResponse.success(data=category_list)
        
    except Exception as e:
        logger.error(f"Error getting document categories: {e}")
        return APIResponse.error(f"获取文档分类失败: {str(e)}", 500)

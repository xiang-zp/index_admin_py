from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
import uuid

from app.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.utils.activity import create_simple_activity
from app.dependencies import get_current_user
from app.models.user import AdminUser

router = APIRouter()
logger = get_logger(__name__)


@router.get("", response_model=dict)
async def get_documents(
    category: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        query = db.query(Document)
        if category:
            query = query.filter(Document.category == category)
        
        total = query.count()
        documents = query.order_by(Document.sort_order).offset((page - 1) * page_size).limit(page_size).all()
        
        return APIResponse.success(data={
            "list": [
                {
                    "id": doc.id,
                    "category": doc.category,
                    "title": doc.title,
                    "description": doc.description,
                    "color": doc.color,
                    "url": doc.url,
                    "row": doc.row,
                    "is_visible": doc.is_visible,
                    "sort_order": doc.sort_order,
                    "created_at": doc.created_at.isoformat() if doc.created_at else None,
                    "updated_at": doc.updated_at.isoformat() if doc.updated_at else None
                }
                for doc in documents
            ],
            "total": total
        })
    except Exception as e:
        logger.error(f"Get documents error: {e}")
        return APIResponse.error(f"获取文档列表失败: {str(e)}", 500)


@router.get("/categories", response_model=dict)
async def get_categories(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        categories = db.query(Document.category).distinct().all()
        result = [
            {"id": str(idx + 1), "name": cat[0]}
            for idx, cat in enumerate(categories)
        ]
        return APIResponse.success(data=result)
    except Exception as e:
        logger.error(f"Get categories error: {e}")
        return APIResponse.error(f"获取分类列表失败: {str(e)}", 500)


@router.post("", response_model=dict)
async def create_document(
    request: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        max_order = db.query(Document).count()
        
        max_id = db.query(Document).filter(Document.id.like('DOC-%')).order_by(Document.id.desc()).first()
        if max_id:
            try:
                num = int(max_id.id.split('-')[1])
                new_num = num + 1
            except:
                new_num = max_order + 1
        else:
            new_num = max_order + 1
        
        doc_id = f"DOC-{new_num:04d}"
        
        document = Document(
            id=doc_id,
            category=request.category,
            title=request.title,
            description=request.description,
            color=request.color,
            url=request.url,
            row=request.row,
            is_visible=request.is_visible,
            sort_order=max_order
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # 记录创建文档活动
        create_simple_activity(
            db=db,
            activity_type="document_create",
            message=f"创建文档 '{document.title}'",
            user_id=current_user.id,
            target_id=document.id,
            target_type="document",
            details={
                "title": document.title,
                "category": document.category,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Document created: {document.id}")
        return APIResponse.success(data={
            "id": document.id,
            "category": document.category,
            "title": document.title,
            "description": document.description,
            "color": document.color,
            "url": document.url,
            "row": document.row,
            "is_visible": document.is_visible,
            "sort_order": document.sort_order,
            "created_at": document.created_at.isoformat() if document.created_at else None,
            "updated_at": document.updated_at.isoformat() if document.updated_at else None
        })
    except Exception as e:
        logger.error(f"Create document error: {e}")
        db.rollback()
        return APIResponse.error(f"创建文档失败: {str(e)}", 500)


@router.put("/{document_id}", response_model=dict)
async def update_document(
    document_id: str,
    request: dict,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return APIResponse.error("文档不存在", 404)
        
        if "category" in request and request["category"] is not None:
            document.category = request["category"]
        if "title" in request and request["title"] is not None:
            document.title = request["title"]
        if "description" in request and request["description"] is not None:
            document.description = request["description"]
        if "color" in request and request["color"] is not None:
            document.color = request["color"]
        if "url" in request and request["url"] is not None:
            document.url = request["url"]
        if "row" in request and request["row"] is not None:
            document.row = request["row"]
        if "is_visible" in request and request["is_visible"] is not None:
            document.is_visible = request["is_visible"]
        
        db.commit()
        db.refresh(document)
        
        # 记录更新文档活动
        create_simple_activity(
            db=db,
            activity_type="document_update",
            message=f"更新文档 '{document.title}'           ",
 user_id=current_user.id,
            target_id=document.id,
            target_type="document",
            details={
                "title": document.title,
                "category": document.category,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Document updated: {document_id}")
        return APIResponse.success(data={
            "id": document.id,
            "category": document.category,
            "title": document.title,
            "description": document.description,
            "color": document.color,
            "url": document.url,
            "row": document.row,
            "is_visible": document.is_visible,
            "sort_order": document.sort_order,
            "created_at": document.created_at.isoformat() if document.created_at else None,
            "updated_at": document.updated_at.isoformat() if document.updated_at else None
        })
    except Exception as e:
        logger.error(f"Update document error: {e}")
        db.rollback()
        return APIResponse.error(f"更新文档失败: {str(e)}", 500)


@router.delete("/{document_id}", response_model=dict)
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return APIResponse.error("文档不存在", 404)
        
        # 记录删除文档活动
        create_simple_activity(
            db=db,
            activity_type="document_delete",
            message=f"删除文档 '{document.title}'",
            user_id=current_user.id,
            target_id=document.id,
            target_type="document",
            details={
                "title": document.title,
                "category": document.category,
                "operator_username": current_user.username
            }
        )
        
        db.delete(document)
        db.commit()
        
        logger.info(f"Document deleted: {document_id}")
        return APIResponse.success(message="删除成功")
    except Exception as e:
        logger.error(f"Delete document error: {e}")
        db.rollback()
        return APIResponse.error(f"删除文档失败: {str(e)}", 500)


@router.patch("/{document_id}/toggle", response_model=dict)
async def toggle_document(
    document_id: str,
    request: dict,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return APIResponse.error("文档不存在", 404)
        
        document.is_visible = request.get("is_visible", True)
        db.commit()
        
        # 记录切换文档状态活动
        create_simple_activity(
            db=db,
            activity_type="document_toggle",
            message=f"设置文档 '{document.title}' 为 {'显示' if document.is_visible else '隐藏'}",
            user_id=current_user.id,
            target_id=document.id,
            target_type="document",
            details={
                "title": document.title,
                "category": document.category,
                "is_visible": document.is_visible,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Document toggled: {document_id}")
        return APIResponse.success(message="状态更新成功")
    except Exception as e:
        logger.error(f"Toggle document error: {e}")
        db.rollback()
        return APIResponse.error(f"切换状态失败: {str(e)}", 500)

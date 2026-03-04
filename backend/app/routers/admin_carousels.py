from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models.carousel import Carousel
from app.schemas.carousel import CarouselCreate, CarouselUpdate, CarouselReorderRequest, CarouselToggleRequest
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.utils.activity import create_simple_activity
from app.dependencies import get_current_user
from app.models.user import AdminUser

router = APIRouter()
logger = get_logger(__name__)


@router.get("", response_model=dict)
async def get_carousels(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        carousels = db.query(Carousel).order_by(Carousel.sort_order).all()
        return APIResponse.success(data=[
            {
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "is_visible": c.is_visible,
                "sort_order": c.sort_order,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "updated_at": c.updated_at.isoformat() if c.updated_at else None
            }
            for c in carousels
        ])
    except Exception as e:
        logger.error(f"Get carousels error: {e}")
        return APIResponse.error(f"获取轮播列表失败: {str(e)}", 500)


@router.post("", response_model=dict)
async def create_carousel(
    request: CarouselCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        max_order = db.query(Carousel).count()
        carousel = Carousel(
            id=f"CAR-{uuid.uuid4().hex[:8].upper()}",
            title=request.title,
            description=request.description,
            is_visible=request.is_visible,
            sort_order=max_order
        )
        db.add(carousel)
        db.commit()
        db.refresh(carousel)
        
        # 记录创建轮播活动
        create_simple_activity(
            db=db,
            activity_type="carousel_create",
            message=f"创建轮播 '{carousel.title}'",
            user_id=current_user.id,
            target_id=carousel.id,
            target_type="carousel",
            details={
                "title": carousel.title,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Carousel created: {carousel.id}")
        return APIResponse.success(data={
            "id": carousel.id,
            "title": carousel.title,
            "description": carousel.description,
            "is_visible": carousel.is_visible,
            "sort_order": carousel.sort_order,
            "created_at": carousel.created_at.isoformat() if carousel.created_at else None,
            "updated_at": carousel.updated_at.isoformat() if carousel.updated_at else None
        })
    except Exception as e:
        logger.error(f"Create carousel error: {e}")
        db.rollback()
        return APIResponse.error(f"创建轮播失败: {str(e)}", 500)


@router.put("/reorder", response_model=dict)
async def reorder_carousels(
    request: CarouselReorderRequest,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        logger.info(f"开始重新排序轮播，ID列表: {request.ids}")
        
        # 调试：获取数据库中所有轮播ID
        all_carousel_ids = [c.id for c in db.query(Carousel).all()]
        logger.info(f"数据库中的轮播ID: {all_carousel_ids}")
        
        # 首先检查所有ID是否存在
        existing_ids = []
        for idx, carousel_id in enumerate(request.ids):
            carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
            if carousel:
                existing_ids.append(carousel_id)
                carousel.sort_order = idx
                logger.info(f"更新轮播 {carousel_id} 排序为 {idx}")
            else:
                logger.warning(f"轮播ID不存在: {carousel_id}")
                return APIResponse.error(f"轮播不存在: {carousel_id}", 404)
        
        db.commit()
        
        # 记录重新排序轮播活动
        create_simple_activity(
            db=db,
            activity_type="carousel_reorder",
            message=f"重新排序轮播图",
            user_id=current_user.id,
            target_id=None,
            target_type="carousel",
            details={
                "count": len(request.ids),
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Carousels reordered")
        return APIResponse.success(message="排序更新成功")
    except Exception as e:
        logger.error(f"Reorder carousels error: {e}")
        db.rollback()
        return APIResponse.error(f"排序更新失败: {str(e)}", 500)


@router.put("/{carousel_id}", response_model=dict)
async def update_carousel(
    carousel_id: str,
    request: CarouselUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
        if not carousel:
            return APIResponse.error("轮播不存在", 404)
        
        if request.title is not None:
            carousel.title = request.title
        if request.description is not None:
            carousel.description = request.description
        if request.is_visible is not None:
            carousel.is_visible = request.is_visible
        
        db.commit()
        db.refresh(carousel)
        
        # 记录更新轮播活动
        create_simple_activity(
            db=db,
            activity_type="carousel_update",
            message=f"更新轮播 '{carousel.title}'",
            user_id=current_user.id,
            target_id=carousel.id,
            target_type="carousel",
            details={
                "title": carousel.title,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Carousel updated: {carousel_id}")
        return APIResponse.success(data={
            "id": carousel.id,
            "title": carousel.title,
            "description": carousel.description,
            "is_visible": carousel.is_visible,
            "sort_order": carousel.sort_order,
            "created_at": carousel.created_at.isoformat() if carousel.created_at else None,
            "updated_at": carousel.updated_at.isoformat() if carousel.updated_at else None
        })
    except Exception as e:
        logger.error(f"Update carousel error: {e}")
        db.rollback()
        return APIResponse.error(f"更新轮播失败: {str(e)}", 500)


@router.delete("/{carousel_id}", response_model=dict)
async def delete_carousel(
    carousel_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
        if not carousel:
            return APIResponse.error("轮播不存在", 404)
        
        # 记录删除轮播活动
        create_simple_activity(
            db=db,
            activity_type="carousel_delete",
            message=f"删除轮播 '{carousel.title}'",
            user_id=current_user.id,
            target_id=carousel.id,
            target_type="carousel",
            details={
                "title": carousel.title,
                "operator_username": current_user.username
            }
        )
        
        db.delete(carousel)
        db.commit()
        
        logger.info(f"Carousel deleted: {carousel_id}")
        return APIResponse.success(message="删除成功")
    except Exception as e:
        logger.error(f"Delete carousel error: {e}")
        db.rollback()
        return APIResponse.error(f"删除轮播失败: {str(e)}", 500)


@router.patch("/{carousel_id}/toggle", response_model=dict)
async def toggle_carousel(
    carousel_id: str,
    request: CarouselToggleRequest,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
        if not carousel:
            return APIResponse.error("轮播不存在", 404)
        
        carousel.is_visible = request.is_visible
        db.commit()
        
        # 记录切换轮播状态活动
        create_simple_activity(
            db=db,
            activity_type="carousel_toggle",
            message=f"设置轮播 '{carousel.title}' 为 {'显示' if carousel.is_visible else '隐藏'}",
            user_id=current_user.id,
            target_id=carousel.id,
            target_type="carousel",
            details={
                "title": carousel.title,
                "is_visible": carousel.is_visible,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Carousel toggled: {carousel_id} -> {request.is_visible}")
        return APIResponse.success(message="状态更新成功")
    except Exception as e:
        logger.error(f"Toggle carousel error: {e}")
        db.rollback()
        return APIResponse.error(f"切换状态失败: {str(e)}", 500)

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.utils.activity import create_simple_activity
from app.dependencies import get_current_user
from app.models.user import AdminUser

router = APIRouter()
logger = get_logger(__name__)


@router.get("", response_model=dict)
async def get_reviews(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        query = db.query(Review)
        total = query.count()
        reviews = query.order_by(Review.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        
        return APIResponse.success(data={
            "list": [
                {
                    "id": review.id,
                    "name": review.name,
                    "avatar_color": review.avatar_color,
                    "rating": review.rating,
                    "content": review.content,
                    "created_at": review.created_at.isoformat() if review.created_at else None,
                    "updated_at": review.updated_at.isoformat() if review.updated_at else None
                }
                for review in reviews
            ],
            "total": total
        })
    except Exception as e:
        logger.error(f"Get reviews error: {e}")
        return APIResponse.error(f"获取评价列表失败: {str(e)}", 500)


@router.post("", response_model=dict)
async def create_review(
    request: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        review = Review(
            id=f"REV-{uuid.uuid4().hex[:8].upper()}",
            name=request.name,
            avatar_color=request.avatar_color,
            rating=request.rating,
            content=request.content
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        
        # 记录创建评价活动
        create_simple_activity(
            db=db,
            activity_type="review_create",
            message=f"创建评价 '{review.name}'",
            user_id=current_user.id,
            target_id=review.id,
            target_type="review",
            details={
                "name": review.name,
                "rating": review.rating,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Review created: {review.id}")
        return APIResponse.success(data={
            "id": review.id,
            "name": review.name,
            "avatar_color": review.avatar_color,
            "rating": review.rating,
            "content": review.content,
            "created_at": review.created_at.isoformat() if review.created_at else None,
            "updated_at": review.updated_at.isoformat() if review.updated_at else None
        })
    except Exception as e:
        logger.error(f"Create review error: {e}")
        db.rollback()
        return APIResponse.error(f"创建评价失败: {str(e)}", 500)


@router.put("/{review_id}", response_model=dict)
async def update_review(
    review_id: str,
    request: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            return APIResponse.error("评价不存在", 404)
        
        if request.name is not None:
            review.name = request.name
        if request.avatar_color is not None:
            review.avatar_color = request.avatar_color
        if request.rating is not None:
            review.rating = request.rating
        if request.content is not None:
            review.content = request.content
        
        db.commit()
        db.refresh(review)
        
        # 记录更新评价活动
        create_simple_activity(
            db=db,
            activity_type="review_update",
            message=f"更新评价 '{review.name}'",
            user_id=current_user.id,
            target_id=review.id,
            target_type="review",
            details={
                "name": review.name,
                "rating": review.rating,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Review updated: {review_id}")
        return APIResponse.success(data={
            "id": review.id,
            "name": review.name,
            "avatar_color": review.avatar_color,
            "rating": review.rating,
            "content": review.content,
            "created_at": review.created_at.isoformat() if review.created_at else None,
            "updated_at": review.updated_at.isoformat() if review.updated_at else None
        })
    except Exception as e:
        logger.error(f"Update review error: {e}")
        db.rollback()
        return APIResponse.error(f"更新评价失败: {str(e)}", 500)


@router.delete("/{review_id}", response_model=dict)
async def delete_review(
    review_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            return APIResponse.error("评价不存在", 404)
        
        # 记录删除评价活动
        create_simple_activity(
            db=db,
            activity_type="review_delete",
            message=f"删除评价 '{review.name}'",
            user_id=current_user.id,
            target_id=review.id,
            target_type="review",
            details={
                "name": review.name,
                "rating": review.rating,
                "operator_username": current_user.username
            }
        )
        
        db.delete(review)
        db.commit()
        
        logger.info(f"Review deleted: {review_id}")
        return APIResponse.success(message="删除成功")
    except Exception as e:
        logger.error(f"Delete review error: {e}")
        db.rollback()
        return APIResponse.error(f"删除评价失败: {str(e)}", 500)

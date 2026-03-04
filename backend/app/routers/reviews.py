from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.review import Review
from app.schemas.review import ReviewResponse, ReviewListResponse, ReviewCreate
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from datetime import datetime
import random
import uuid

router = APIRouter()
logger = get_logger(__name__)

# 生成随机头像颜色
AVATAR_COLORS = [
    "#6C5CE7", "#FD79A8", "#FDC12A", "#00B894", "#E17055",
    "#0984E3", "#2196F3", "#9C27B0", "#FF5722", "#4CAF50"
]


@router.get("/", response_model=dict)
async def get_reviews(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取评价列表
    """
    try:
        query = db.query(Review)
        
        # 获取总数
        total = query.count()
        
        # 分页查询
        items = query.order_by(Review.created_at.desc()).offset(
            (page - 1) * page_size
        ).limit(page_size).all()
        
        review_list = [
            ReviewResponse(
                id=review.id,
                name=review.name,
                avatar=review.name[:2].upper() if review.name else "U",
                avatar_color=review.avatar_color,
                rating=review.rating,
                date=review.created_at.strftime("%Y年%m月%d日"),
                content=review.content
            )
            for review in items
        ]
        
        return APIResponse.success(
            data=ReviewListResponse(
                list=review_list,
                total=total,
                page=page,
                page_size=page_size
            )
        )
        
    except Exception as e:
        logger.error(f"Error getting reviews: {e}")
        return APIResponse.error(f"获取评价列表失败: {str(e)}", 500)


@router.post("/", response_model=dict)
async def create_review(
    request: ReviewCreate,
    db: Session = Depends(get_db)
):
    """
    提交评价
    """
    try:
        # 随机选择头像颜色
        avatar_color = random.choice(AVATAR_COLORS)
        
        # 生成唯一ID
        review_id = f"REV-{uuid.uuid4().hex[:8].upper()}"
        
        # 创建评价
        review = Review(
            id=review_id,
            name=request.name,
            avatar_color=avatar_color,
            rating=request.rating,
            content=request.content
        )
        
        db.add(review)
        db.commit()
        db.refresh(review)
        
        logger.info(f"Review created: {review.id}")
        
        return APIResponse.success(
            data=ReviewResponse(
                id=review.id,
                name=review.name,
                avatar=review.name[:2].upper() if review.name else "U",
                avatar_color=review.avatar_color,
                rating=review.rating,
                date=review.created_at.strftime("%Y年%m月%d日"),
                content=review.content
            ),
            message="评价提交成功"
        )
        
    except Exception as e:
        logger.error(f"Error creating review: {e}")
        db.rollback()
        return APIResponse.error(f"提交评价失败: {str(e)}", 500)

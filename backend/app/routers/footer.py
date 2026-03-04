from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.footer import FooterConfig, FooterLink
from app.utils.response import APIResponse
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/config", response_model=dict)
async def get_footer_config(db: Session = Depends(get_db)):
    """
    获取底部配置（公开接口）
    """
    try:
        config = db.query(FooterConfig).first()
        if not config:
            config = FooterConfig(id=1)
            db.add(config)
            db.commit()
            db.refresh(config)
        
        return APIResponse.success(data={
            "logo_url": config.logo_url,
            "slogan": config.slogan,
            "updated_at": config.updated_at.isoformat() if config.updated_at else None
        })
    except Exception as e:
        logger.error(f"Get footer config error: {e}")
        return APIResponse.error(f"获取底部配置失败: {str(e)}", 500)


@router.get("/links", response_model=dict)
async def get_footer_links(db: Session = Depends(get_db)):
    """
    获取底部链接列表（公开接口）
    """
    try:
        links = db.query(FooterLink).order_by(FooterLink.sort_order).all()
        return APIResponse.success(data=[
            {
                "id": link.id,
                "title": link.title,
                "url": link.url,
                "sort_order": link.sort_order,
                "created_at": link.created_at.isoformat() if link.created_at else None,
                "updated_at": link.updated_at.isoformat() if link.updated_at else None
            }
            for link in links
        ])
    except Exception as e:
        logger.error(f"Get footer links error: {e}")
        return APIResponse.error(f"获取底部链接失败: {str(e)}", 500)

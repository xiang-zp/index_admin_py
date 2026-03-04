from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models.footer import FooterConfig, FooterLink
from app.schemas.footer import FooterConfigUpdate, FooterLinkCreate, FooterLinkUpdate
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.utils.activity import create_simple_activity
from app.dependencies import get_current_user
from app.models.user import AdminUser

router = APIRouter()
logger = get_logger(__name__)

def _ensure_footer_logo_url_longtext(db: Session) -> None:
    dialect = getattr(getattr(db, "bind", None), "dialect", None)
    dialect_name = getattr(dialect, "name", "")

    if dialect_name != "mysql":
        return

    try:
        current = db.execute(
            text(
                """
                SELECT data_type, character_maximum_length
                FROM information_schema.columns
                WHERE table_schema = DATABASE()
                  AND table_name = 'footer_config'
                  AND column_name = 'logo_url'
                """
            )
        ).fetchone()

        if not current:
            return

        data_type = (current[0] or "").lower()
        char_len = current[1]

        if data_type in {"text", "mediumtext", "longtext"}:
            return
        if isinstance(char_len, int) and char_len >= 4000:
            return

        db.execute(text("ALTER TABLE footer_config MODIFY logo_url LONGTEXT NULL"))
        db.commit()
    except Exception as e:
        logger.error(f"Ensure footer_config.logo_url LONGTEXT error: {e}")
        db.rollback()


@router.get("/config", response_model=dict)
async def get_footer_config(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
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


@router.put("/config", response_model=dict)
async def update_footer_config(
    request: FooterConfigUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        config = db.query(FooterConfig).first()
        if not config:
            config = FooterConfig(id=1)
            db.add(config)
        
        if request.logo_url is not None:
            if isinstance(request.logo_url, str) and len(request.logo_url) > 500:
                _ensure_footer_logo_url_longtext(db)
            config.logo_url = request.logo_url
        if request.slogan is not None:
            config.slogan = request.slogan
        
        db.commit()
        db.refresh(config)
        
        # 记录更新底部配置活动
        create_simple_activity(
            db=db,
            activity_type="footer_config_update",
            message=f"更新底部配置",
            user_id=current_user.id,
            target_id=str(config.id),
            target_type="footer_config",
            details={
                "has_logo_update": request.logo_url is not None,
                "has_slogan_update": request.slogan is not None,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Footer config updated")
        return APIResponse.success(data={
            "logo_url": config.logo_url,
            "slogan": config.slogan,
            "updated_at": config.updated_at.isoformat() if config.updated_at else None
        })
    except Exception as e:
        logger.error(f"Update footer config error: {e}")
        db.rollback()
        return APIResponse.error(f"更新底部配置失败: {str(e)}", 500)


@router.get("/links", response_model=dict)
async def get_footer_links(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
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


@router.post("/links", response_model=dict)
async def create_footer_link(
    request: FooterLinkCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        max_order = db.query(FooterLink).count()
        link = FooterLink(
            id=f"LINK-{uuid.uuid4().hex[:8].upper()}",
            title=request.title,
            url=request.url,
            sort_order=max_order
        )
        db.add(link)
        db.commit()
        db.refresh(link)
        
        # 记录创建底部链接活动
        create_simple_activity(
            db=db,
            activity_type="footer_link_create",
            message=f"创建底部链接 '{link.title}'",
            user_id=current_user.id,
            target_id=link.id,
            target_type="footer_link",
            details={
                "title": link.title,
                "url": link.url,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Footer link created: {link.id}")
        return APIResponse.success(data={
            "id": link.id,
            "title": link.title,
            "url": link.url,
            "sort_order": link.sort_order,
            "created_at": link.created_at.isoformat() if link.created_at else None,
            "updated_at": link.updated_at.isoformat() if link.updated_at else None
        })
    except Exception as e:
        logger.error(f"Create footer link error: {e}")
        db.rollback()
        return APIResponse.error(f"创建底部链接失败: {str(e)}", 500)


@router.put("/links/{link_id}", response_model=dict)
async def update_footer_link(
    link_id: str,
    request: FooterLinkUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        link = db.query(FooterLink).filter(FooterLink.id == link_id).first()
        if not link:
            return APIResponse.error("链接不存在", 404)
        
        if request.title is not None:
            link.title = request.title
        if request.url is not None:
            link.url = request.url
        
        db.commit()
        db.refresh(link)
        
        # 记录更新底部链接活动
        create_simple_activity(
            db=db,
            activity_type="footer_link_update",
            message=f"更新底部链接 '{link.title}'",
            user_id=current_user.id,
            target_id=link.id,
            target_type="footer_link",
            details={
                "title": link.title,
                "url": link.url,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Footer link updated: {link_id}")
        return APIResponse.success(data={
            "id": link.id,
            "title": link.title,
            "url": link.url,
            "sort_order": link.sort_order,
            "created_at": link.created_at.isoformat() if link.created_at else None,
            "updated_at": link.updated_at.isoformat() if link.updated_at else None
        })
    except Exception as e:
        logger.error(f"Update footer link error: {e}")
        db.rollback()
        return APIResponse.error(f"更新底部链接失败: {str(e)}", 500)


@router.delete("/links/{link_id}", response_model=dict)
async def delete_footer_link(
    link_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        link = db.query(FooterLink).filter(FooterLink.id == link_id).first()
        if not link:
            return APIResponse.error("链接不存在", 404)
        
        # 记录删除底部链接活动
        create_simple_activity(
            db=db,
            activity_type="footer_link_delete",
            message=f"删除底部链接 '{link.title}'",
            user_id=current_user.id,
            target_id=link.id,
            target_type="footer_link",
            details={
                "title": link.title,
                "url": link.url,
                "operator_username": current_user.username
            }
        )
        
        db.delete(link)
        db.commit()
        
        logger.info(f"Footer link deleted: {link_id}")
        return APIResponse.success(message="删除成功")
    except Exception as e:
        logger.error(f"Delete footer link error: {e}")
        db.rollback()
        return APIResponse.error(f"删除底部链接失败: {str(e)}", 500)

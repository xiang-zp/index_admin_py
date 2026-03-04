# -*- coding: utf-8 -*-
"""
FastAPI 主应用模块

智能问答平台后端 API 入口点。
负责初始化应用、配置中间件、注册路由等。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.config import settings
from app.utils.logger import get_logger
from app.routers import auth
from app.routers import admin_agents, admin_tools, admin_documents, admin_document_categories, admin_reviews, admin_auth_codes, admin_auth_locations, admin_users, admin_carousels, admin_footer, admin_dashboard
from app.routers import chat, tools, reviews, documents, projects, carousels, footer


logger = get_logger(__name__)


# 创建 FastAPI 应用实例
app = FastAPI(
    title="Smart QA Backend API",
    description="智能问答平台后端 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=False
)


# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


# 挂载静态文件目录 - 图片服务
IMAGE_DIR = Path(__file__).parent.parent / "database" / "image"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/database/image", StaticFiles(directory=str(IMAGE_DIR), html=True), name="image_static")


# 注册路由
# 认证模块
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])

# 聊天模块
app.include_router(chat.router, prefix="/api/chat", tags=["聊天"])

# 工具模块
app.include_router(tools.router, prefix="/api/tools", tags=["工具"])

# 评价模块
app.include_router(reviews.router, prefix="/api/reviews", tags=["评价"])

# 文档模块
app.include_router(documents.router, prefix="/api/documents", tags=["文档"])

# 项目模块
app.include_router(projects.router, prefix="/api/projects", tags=["项目"])

# 轮播文案模块
app.include_router(carousels.router, prefix="/api/carousels", tags=["滚动消息"])

# 底部配置模块
app.include_router(footer.router, prefix="/api/footer", tags=["底部配置"])

# ===== 管理后台模块 =====

# 智能体管理
app.include_router(admin_agents.router, prefix="/api/admin/agents", tags=["智能体管理"])

# 开源项目管理
app.include_router(admin_tools.router, prefix="/api/admin/tools", tags=["开源项目管理"])

# 文档资料管理
app.include_router(admin_documents.router, prefix="/api/admin/documents", tags=["文档资料管理"])

# 文档分类管理
app.include_router(admin_document_categories.router, prefix="/api/admin/document-categories", tags=["文档分类管理"])

# 用户评价管理
app.include_router(admin_reviews.router, prefix="/api/admin/reviews", tags=["用户评价管理"])

# 授权码管理
app.include_router(admin_auth_codes.router, prefix="/api/admin/auth-codes", tags=["授权码管理"])

# 授权位置管理
app.include_router(admin_auth_locations.router, prefix="/api/admin/auth-locations", tags=["授权位置管理"])

# 用户管理
app.include_router(admin_users.router, prefix="/api/admin/users", tags=["用户管理"])

# 轮播文案管理
app.include_router(admin_carousels.router, prefix="/api/admin/carousels", tags=["轮播文案管理"])

# 底部配置管理
app.include_router(admin_footer.router, prefix="/api/admin/footer", tags=["底部配置管理"])

# 仪表盘统计
app.include_router(admin_dashboard.router, prefix="/api/admin/dashboard", tags=["仪表盘统计"])


@app.get("/")
async def root():
    """
    根路由

    返回API基本信息。
    """
    return {
        "message": "Smart QA Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    健康检查接口

    用于服务健康检测和负载均衡探测。
    """
    return {
        "status": "healthy",
        "environment": settings.APP_ENV
    }


# 启动入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.APP_ENV == "development"
    )

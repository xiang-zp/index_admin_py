# Smart QA Backend

智能问答平台后端服务，基于 FastAPI 框架开发，提供完整的 RESTful API 接口。

## 项目介绍

Smart QA Backend 是一个面向智能问答平台的后端管理系统，支持用户认证、智能对话、项目推荐、文档管理、用户评价等功能。系统采用前后端分离架构，提供完善的 API 接口供前端调用。

### 主要功能

- **用户认证**：JWT Token 身份验证，支持邀请码授权管理
- **智能对话**：SSE 流式响应，支持多智能体切换
- **项目管理**：推荐项目分类展示，支持可见性控制
- **文档管理**：文档资料分类管理，支持分类筛选
- **用户评价**：用户评价展示与提交
- **底部配置**：网站底部 Logo、Slogan、链接配置
- **轮播文案**：首页轮播内容管理
- **管理后台**：完整的后台管理系统，支持 CRUD 操作
- **仪表盘统计**：数据统计与活动记录

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.11+ | 后端语言 |
| FastAPI | 0.104+ | Web 框架 |
| SQLAlchemy | 2.0+ | ORM 框架 |
| MySQL | 8.0+ | 关系型数据库 |
| Pydantic | 2.0+ | 数据验证 |
| Uvicorn | 0.24+ | ASGI 服务器 |
| JWT | - | 用户认证 |
| bcrypt | - | 密码加密 |

## 项目结构

```
backend/
├── app/
│   ├── main.py                    # FastAPI 应用入口
│   ├── config.py                  # 配置文件（环境变量管理）
│   ├── database.py                # 数据库连接（SQLAlchemy 配置）
│   ├── dependencies.py            # 依赖注入（认证中间件）
│   ├── models/                    # SQLAlchemy 数据模型
│   │   ├── user.py               # 管理员用户模型
│   │   ├── agent.py              # 智能体模型
│   │   ├── tool.py               # 工具/项目模型
│   │   ├── document.py           # 文档模型
│   │   ├── document_category.py  # 文档分类模型
│   │   ├── review.py             # 用户评价模型
│   │   ├── carousel.py           # 轮播文案模型
│   │   ├── footer.py             # 底部配置模型
│   │   ├── conversation.py        # 对话模型
│   │   ├── message.py            # 消息模型
│   │   ├── activity.py           # 活动记录模型
│   │   ├── auth_code.py          # 授权码模型
│   │   └── auth_location.py     # 授权位置模型
│   ├── schemas/                   # Pydantic 数据模型（请求/响应）
│   ├── routers/                   # API 路由
│   │   ├── auth.py               # 认证接口
│   │   ├── chat.py               # 聊天接口
│   │   ├── tools.py              # 工具列表接口
│   │   ├── projects.py           # 项目推荐接口
│   │   ├── documents.py          # 文档列表接口
│   │   ├── reviews.py            # 用户评价接口
│   │   ├── carousels.py          # 轮播文案接口
│   │   ├── footer.py             # 底部配置接口
│   │   ├── admin_*.py            # 管理后台接口（12个模块）
│   │   └── stats.py              # 统计接口
│   └── utils/                     # 工具函数
│       ├── auth.py                # 认证工具（密码哈希、JWT）
│       ├── response.py            # 响应格式化
│       ├── logger.py              # 日志工具
│       └── activity.py            # 活动记录工具
├── scripts/                       # 工具脚本
│   ├── init_db.py                # 数据库初始化
│   ├── update_password.py         # 密码更新
│   └── test_*.py                 # 测试脚本
├── tests/                         # 测试目录
├── requirements.txt               # Python 依赖
├── .env                          # 环境变量配置
├── .env.example                  # 环境变量示例
└── README.md                     # 项目文档
```

## 环境配置

### 1. 创建虚拟环境

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 到 `.env` 并根据实际情况修改：

```bash
cp .env.example .env
```

`.env` 文件配置说明：

```env
# 数据库配置（MySQL）
DATABASE_URL=mysql+pymysql://root:password@host:port/database_name

# 应用环境（development / production）
APP_ENV=development

# 日志级别
LOG_LEVEL=INFO

# CORS 配置（多个域名用逗号分隔）
CORS_ORIGINS=http://localhost:5173,http://localhost:5174,http://localhost:5175

# LLM 配置
LLM_API_KEY=your_api_key_here
LLM_MODEL=doubao

# JWT 配置
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### 4. 数据库初始化

确保 MySQL 数据库已创建，然后运行初始化脚本：

```bash
python scripts/init_db.py
```

## 启动服务

### 开发环境（推荐）

```bash
# 方式一：使用 uvicorn 命令
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 方式二：直接运行 main.py
python -m app.main
```

服务启动后，访问以下地址：

| 服务 | 地址 |
|------|------|
| API 文档 (Swagger) | http://localhost:8000/docs |
| API 文档 (ReDoc) | http://localhost:8000/redoc |
| 健康检查 | http://localhost:8000/health |
| 根路由 | http://localhost:8000/ |

### 生产环境

```bash
# 使用 uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 或使用 gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API 接口文档

### 公开接口

#### 1. 认证接口 `/api/auth`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/verify | 验证邀请码 |
| POST | /api/auth/revoke | 取消授权 |

#### 2. 聊天接口 `/api/chat`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/chat/agents | 获取智能体列表 |
| POST | /api/chat/send | 发送消息（SSE 流式） |
| POST | /api/chat/terminate | 终止对话任务 |

#### 3. 工具接口 `/api/tools`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/tools/ | 获取工具列表 |

#### 4. 项目接口 `/api/projects`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/projects | 获取项目列表 |
| GET | /api/projects/categories | 获取项目分类 |

#### 5. 文档接口 `/api/documents`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/documents/ | 获取文档列表 |
| GET | /api/documents/categories | 获取文档分类 |

#### 6. 评价接口 `/api/reviews`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/reviews/ | 获取评价列表 |
| POST | /api/reviews/ | 提交评价 |

#### 7. 轮播接口 `/api/carousels`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/carousels/ | 获取轮播列表 |

#### 8. 底部配置接口 `/api/footer`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/footer/config | 获取底部配置 |
| GET | /api/footer/links | 获取底部链接 |

### 管理后台接口（需认证）

#### 9. 仪表盘 `/api/admin/dashboard`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/dashboard/stats | 获取统计信息 |
| GET | /api/admin/dashboard/activities | 获取活动记录 |

#### 10. 用户管理 `/api/admin/users`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/users | 获取用户列表 |
| GET | /api/admin/users/{user_id} | 获取单个用户 |
| POST | /api/admin/users | 创建用户 |
| PUT | /api/admin/users/{user_id} | 更新用户 |
| DELETE | /api/admin/users/{user_id} | 删除用户 |

#### 11. 智能体管理 `/api/admin/agents`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/agents | 获取智能体列表 |
| POST | /api/admin/agents | 创建智能体 |
| PUT | /api/admin/agents/{agent_id} | 更新智能体 |
| DELETE | /api/admin/agents/{agent_id} | 删除智能体 |

#### 12. 工具管理 `/api/admin/tools`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/tools | 获取工具列表 |
| GET | /api/admin/tools/{tool_id} | 获取单个工具 |
| POST | /api/admin/tools | 创建工具 |
| PUT | /api/admin/tools/{tool_id} | 更新工具 |
| DELETE | /api/admin/tools/{tool_id} | 删除工具 |

#### 13. 文档管理 `/api/admin/documents`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/documents | 获取文档列表 |
| GET | /api/admin/documents/categories | 获取文档分类 |
| POST | /api/admin/documents | 创建文档 |
| PUT | /api/admin/documents/{document_id} | 更新文档 |
| DELETE | /api/admin/documents/{document_id} | 删除文档 |

#### 14. 文档分类管理 `/api/admin/document-categories`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/document-categories | 获取分类列表 |
| POST | /api/admin/document-categories | 创建分类 |
| PUT | /api/admin/document-categories/{category_id} | 更新分类 |
| DELETE | /api/admin/document-categories/{category_id} | 删除分类 |

#### 15. 评价管理 `/api/admin/reviews`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/reviews | 获取评价列表 |
| POST | /api/admin/reviews | 创建评价 |
| PUT | /api/admin/reviews/{review_id} | 更新评价 |
| DELETE | /api/admin/reviews/{review_id} | 删除评价 |

#### 16. 授权码管理 `/api/admin/auth-codes`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/auth-codes | 获取授权码列表 |
| POST | /api/admin/auth-codes | 创建授权码 |
| PUT | /api/admin/auth-codes/{auth_code_id} | 更新授权码 |
| DELETE | /api/admin/auth-codes/{auth_code_id} | 删除授权码 |
| POST | /api/admin/auth-codes/{auth_code_id}/revoke | 撤销授权码 |

#### 17. 授权位置管理 `/api/admin/auth-locations`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/auth-locations | 获取授权位置列表 |

#### 18. 轮播管理 `/api/admin/carousels`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/carousels | 获取轮播列表 |
| POST | /api/admin/carousels | 创建轮播 |
| PUT | /api/admin/carousels/{carousel_id} | 更新轮播 |
| DELETE | /api/admin/carousels/{carousel_id} | 删除轮播 |

#### 19. 底部配置管理 `/api/admin/footer`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/footer/config | 获取底部配置 |
| PUT | /api/admin/footer/config | 更新底部配置 |
| GET | /api/admin/footer/links | 获取链接列表 |
| POST | /api/admin/footer/links | 创建链接 |
| PUT | /api/admin/footer/links/{link_id} | 更新链接 |
| DELETE | /api/admin/footer/links/{link_id} | 删除链接 |

## 开发指南

### 添加新模块

1. 在 `app/models/` 创建数据模型
2. 在 `app/schemas/` 创建 Pydantic 模型
3. 在 `app/routers/` 创建路由文件
4. 在 `app/main.py` 注册路由

### 数据库迁移

```bash
# 安装 alembic（如果需要）
pip install alembic

# 初始化 alembic
alembic init alembic

# 生成迁移
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head
```

### 运行测试

```bash
pytest tests/
```

## 常见问题

### 1. 数据库连接失败

检查 `.env` 中的 `DATABASE_URL` 配置是否正确，确保 MySQL 服务已启动。

### 2. CORS 跨域错误

在 `.env` 中配置正确的 `CORS_ORIGINS`，多个域名用逗号分隔。

### 3. JWT Token 过期

检查 `.env` 中的 `JWT_EXPIRATION_HOURS` 配置，或重新登录获取新 Token。

### 4. pip 安装依赖失败（macOS ARM / Python 3.12）

如果遇到 `pydantic-core` 或 `uvloop` 版本不兼容问题：

```bash
# 升级 pip
pip install --upgrade pip

# 修改 requirements.txt，去掉 uvicorn 的 standard 扩展
# 将 uvicorn[standard]==0.24.0 改为 uvicorn==0.24.0
```

### 5. 虚拟环境创建与激活

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t smart-qa-backend .

# 运行容器
docker run -p 8000:8000 --env-file .env smart-qa-backend
```

### Docker Compose 部署

```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: smart_qa
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## License

MIT License

# 后台管理系统 API 接口文档

## 基础信息

| 项目 | 说明 |
|-----|------|
| Base URL | `/api` |
| 认证方式 | Bearer Token (JWT) |
| 请求头 | `Authorization: Bearer <token>` |
| Content-Type | `application/json` |

### 统一响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

### 错误码说明

| 错误码 | 说明 |
|-------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权/Token过期 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 1. 认证模块 (Auth)

### 1.1 管理员登录

- **POST** `/auth/admin/login`
- **无需认证**

**请求体：**

```json
{
  "username": "string",
  "password": "string"
}
```

**响应：**

```json
{
  "code": 0,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "USER-001",
      "username": "admin",
      "role": "admin"
    }
  }
}
```

### 1.2 管理员登出

- **POST** `/auth/admin/logout`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "message": "登出成功"
}
```

### 1.3 获取当前用户信息

- **GET** `/auth/admin/profile`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "data": {
    "id": "USER-001",
    "username": "admin",
    "role": "admin",
    "created_at": "2024-01-01T00:00:00Z",
    "last_login_at": "2024-02-12T10:30:00Z"
  }
}
```

---

## 2. 智能体管理 (Agents)

### 2.1 获取智能体列表

- **GET** `/admin/agents`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "data": [
    {
      "id": "AGENT-001",
      "name": "智能客服",
      "api": "https://api.coze.com/v1/chat",
      "source": "内置",
      "bot_id": "7348xxxxxx",
      "is_visible": true,
      "sort_order": 0,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | string | 智能体ID |
| name | string | 智能体名称 |
| api | string | API调用地址 |
| source | string | 来源：内置/第三方 |
| bot_id | string | Coze智能体ID，用于对接Coze接口 |
| is_visible | boolean | 是否展示 |
| sort_order | number | 排序序号 |

### 2.2 创建智能体

- **POST** `/admin/agents`
- **需要认证**

**请求体：**

```json
{
  "name": "智能客服",
  "api": "https://api.coze.com/v1/chat",
  "source": "内置",
  "bot_id": "7348xxxxxx",
  "is_visible": true
}
```

**响应：**

```json
{
  "code": 0,
  "data": {
    "id": "AGENT-002",
    "name": "智能客服",
    "api": "https://api.coze.com/v1/chat",
    "source": "内置",
    "bot_id": "7348xxxxxx",
    "is_visible": true,
    "sort_order": 1,
    "created_at": "2024-02-12T10:30:00Z",
    "updated_at": "2024-02-12T10:30:00Z"
  }
}
```

### 2.3 更新智能体

- **PUT** `/admin/agents/{id}`
- **需要认证**

**请求体：**

```json
{
  "name": "智能客服",
  "api": "https://api.coze.com/v1/chat",
  "source": "内置",
  "bot_id": "7348xxxxxx",
  "is_visible": true
}
```

### 2.4 删除智能体

- **DELETE** `/admin/agents/{id}`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "message": "删除成功"
}
```

### 2.5 切换展示状态

- **PATCH** `/admin/agents/{id}/toggle`
- **需要认证**

**请求体：**

```json
{
  "is_visible": false
}
```

---

## 3. 开源项目管理 (Tools)

### 3.1 获取项目列表

- **GET** `/admin/tools`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "data": [
    {
      "id": "TOOL-001",
      "title": "Python爬虫工具",
      "description": "强大的Python爬虫工具，支持多种网站抓取",
      "image": "https://example.com/image.jpg",
      "is_visible": true,
      "sort_order": 0,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 3.2 创建项目

- **POST** `/admin/tools`
- **需要认证**

**请求体：**

```json
{
  "title": "Python爬虫工具",
  "description": "强大的Python爬虫工具，支持多种网站抓取",
  "image": "https://example.com/image.jpg",
  "is_visible": true
}
```

### 3.3 更新项目

- **PUT** `/admin/tools/{id}`
- **需要认证**

### 3.4 删除项目

- **DELETE** `/admin/tools/{id}`
- **需要认证**

### 3.5 切换展示状态

- **PATCH** `/admin/tools/{id}/toggle`
- **需要认证**

**请求体：**

```json
{
  "is_visible": false
}
```

---

## 4. 文档资料管理 (Documents)

### 4.1 获取文档列表

- **GET** `/admin/documents`
- **需要认证**

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| category | string | 否 | 分类筛选 |
| page | number | 否 | 页码，默认1 |
| page_size | number | 否 | 每页条数，默认10 |

**响应：**

```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "id": "DOC-001",
        "category": "Python教程",
        "title": "Python基础入门",
        "description": "从零开始学习Python编程语言",
        "date": "2024-02-10",
        "color": "#3b82f6",
        "is_visible": true,
        "sort_order": 0,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 100
  }
}
```

### 4.2 获取分类列表

- **GET** `/admin/documents/categories`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "data": [
    { "id": "1", "name": "Python教程" },
    { "id": "2", "name": "AI应用" },
    { "id": "3", "name": "工具配置" },
    { "id": "4", "name": "最佳实践" }
  ]
}
```

### 4.3 创建文档

- **POST** `/admin/documents`
- **需要认证**

**请求体：**

```json
{
  "category": "Python教程",
  "title": "Python基础入门",
  "description": "从零开始学习Python编程语言",
  "date": "2024-02-10",
  "color": "#3b82f6",
  "is_visible": true
}
```

**color 可选值：**

| 颜色 | 值 |
|-----|-----|
| 蓝色 | #3b82f6 |
| 绿色 | #10b981 |
| 橙色 | #f59e0b |
| 红色 | #ef4444 |
| 紫色 | #8b5cf6 |
| 粉色 | #ec4899 |

### 4.4 更新文档

- **PUT** `/admin/documents/{id}`
- **需要认证**

### 4.5 删除文档

- **DELETE** `/admin/documents/{id}`
- **需要认证**

### 4.6 切换展示状态

- **PATCH** `/admin/documents/{id}/toggle`
- **需要认证**

---

## 5. 用户评价管理 (Reviews)

### 5.1 获取评价列表

- **GET** `/admin/reviews`
- **需要认证**

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| page | number | 否 | 页码，默认1 |
| page_size | number | 否 | 每页条数，默认10 |

**响应：**

```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "id": "REV-001",
        "name": "张先生",
        "avatar_color": "indigo",
        "rating": 5,
        "content": "这个平台非常强大，效率提升了很多！",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 100
  }
}
```

**avatar_color 可选值：**

| 值 | 颜色 |
|-----|------|
| indigo | 靛蓝 |
| emerald | 翡翠 |
| rose | 玫瑰 |
| amber | 琥珀 |
| violet | 紫罗兰 |
| teal | 青色 |

**rating 范围：** 1-5

### 5.2 创建评价

- **POST** `/admin/reviews`
- **需要认证**

**请求体：**

```json
{
  "name": "张先生",
  "avatar_color": "indigo",
  "rating": 5,
  "content": "这个平台非常强大，效率提升了很多！"
}
```

### 5.3 更新评价

- **PUT** `/admin/reviews/{id}`
- **需要认证**

### 5.4 删除评价

- **DELETE** `/admin/reviews/{id}`
- **需要认证**

---

## 6. 授权码管理 (AuthCodes)

### 6.1 获取授权码列表

- **GET** `/admin/auth-codes`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "data": [
    {
      "id": "AUTH-0001",
      "description": "管理员长期授权",
      "invite_code": "sqm12345",
      "status": "authorized",
      "auth_location": "global",
      "authorized_user": "zhangsan",
      "authorized_at": "2024-02-10T00:00:00Z",
      "expire_time": "2025-02-10T00:00:00Z",
      "created_at": "2024-01-15T00:00:00Z",
      "updated_at": "2024-01-15T00:00:00Z"
    }
  ]
}
```

**status 枚举值：**

| 值 | 说明 |
|-----|------|
| authorized | 已授权 |
| expired | 已过期 |
| revoked | 已撤销 |

**auth_location 枚举值：**

| 值 | 说明 |
|-----|------|
| global | 全局（所有功能） |
| agents | 智能体管理 |
| tools | 开源项目 |
| documents | 文档资料 |

### 6.2 创建授权码

- **POST** `/admin/auth-codes`
- **需要认证**

**请求体：**

```json
{
  "description": "管理员长期授权",
  "invite_code": "sqm12345",
  "auth_location": "global",
  "start_date": "2024-02-12T10:00:00Z",
  "end_date": "2025-02-12T10:00:00Z"
}
```

### 6.3 更新授权码

- **PUT** `/admin/auth-codes/{id}`
- **需要认证**

**请求体：**

```json
{
  "description": "管理员长期授权",
  "auth_location": "global",
  "expire_time": "2025-02-12T10:00:00Z"
}
```

### 6.4 删除授权码

- **DELETE** `/admin/auth-codes/{id}`
- **需要认证**

### 6.5 撤销授权

- **POST** `/admin/auth-codes/{id}/revoke`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "message": "授权已撤销"
}
```

---

## 7. 用户管理 (Users)

### 7.1 获取用户列表

- **GET** `/admin/users`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "data": [
    {
      "id": "USER-001",
      "username": "admin",
      "password": "admin123",
      "role": "admin",
      "last_login_at": "2024-02-12T10:30:00Z",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

**role 枚举值：**

| 值 | 说明 |
|-----|------|
| admin | 管理员 |
| editor | 编辑 |
| viewer | 只读 |

### 7.2 获取用户详情

- **GET** `/admin/users/{id}`
- **需要认证**

### 7.3 创建用户

- **POST** `/admin/users`
- **需要认证**

**请求体：**

```json
{
  "username": "editor01",
  "password": "editor123",
  "role": "editor"
}
```

### 7.4 更新用户

- **PUT** `/admin/users/{id}`
- **需要认证**

**请求体：**

```json
{
  "username": "editor01",
  "password": "newpassword",
  "role": "editor"
}
```

> 注：password 字段可选，不传则不修改密码

### 7.5 删除用户

- **DELETE** `/admin/users/{id}`
- **需要认证**

---

## 8. 轮播文案管理 (Carousels)

### 8.1 获取轮播列表

- **GET** `/admin/carousels`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "data": [
    {
      "id": "CAR-001",
      "title": "欢迎使用智能助手",
      "description": "为您提供精准、高效的信息检索服务",
      "is_visible": true,
      "sort_order": 0,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 8.2 创建轮播

- **POST** `/admin/carousels`
- **需要认证**

**请求体：**

```json
{
  "title": "欢迎使用智能助手",
  "description": "为您提供精准、高效的信息检索服务",
  "is_visible": true
}
```

### 8.3 更新轮播

- **PUT** `/admin/carousels/{id}`
- **需要认证**

### 8.4 删除轮播

- **DELETE** `/admin/carousels/{id}`
- **需要认证**

### 8.5 切换展示状态

- **PATCH** `/admin/carousels/{id}/toggle`
- **需要认证**

**请求体：**

```json
{
  "is_visible": false
}
```

### 8.6 拖拽排序

- **PUT** `/admin/carousels/reorder`
- **需要认证**

**请求体：**

```json
{
  "ids": ["CAR-003", "CAR-001", "CAR-002"]
}
```

> 注：ids 数组中的顺序即为新的排序顺序

---

## 9. 底部配置管理 (Footer)

### 9.1 获取底部配置

- **GET** `/admin/footer-config`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "data": {
    "logo_url": "https://example.com/logo.png",
    "slogan": "智能搜索助手，为您提供精准，高效的信息检索服务。",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

### 9.2 更新底部配置

- **PUT** `/admin/footer-config`
- **需要认证**

**请求体：**

```json
{
  "logo_url": "https://example.com/logo.png",
  "slogan": "智能搜索助手，为您提供精准，高效的信息检索服务。"
}
```

### 9.3 获取底部链接列表

- **GET** `/admin/footer-links`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "data": [
    {
      "id": "LINK-001",
      "title": "AI工具集",
      "url": "https://www.deepseek.com/",
      "sort_order": 0,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 9.4 创建底部链接

- **POST** `/admin/footer-links`
- **需要认证**

**请求体：**

```json
{
  "title": "AI工具集",
  "url": "https://www.deepseek.com/"
}
```

### 9.5 更新底部链接

- **PUT** `/admin/footer-links/{id}`
- **需要认证**

**请求体：**

```json
{
  "title": "AI工具集",
  "url": "https://www.deepseek.com/"
}
```

### 9.6 删除底部链接

- **DELETE** `/admin/footer-links/{id}`
- **需要认证**

---

## 10. 仪表盘统计 (Dashboard)

### 10.1 获取统计数据

- **GET** `/admin/dashboard/stats`
- **需要认证**

**响应：**

```json
{
  "code": 0,
  "data": {
    "agents": 5,
    "tools": 12,
    "documents": 48,
    "reviews": 126,
    "users": 8
  }
}
```

### 10.2 获取最近活动

- **GET** `/admin/dashboard/activities`
- **需要认证**

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| limit | number | 否 | 返回条数，默认10 |

**响应：**

```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "type": "agent",
      "message": "新增智能体 \"智能客服\"",
      "time": "2024-02-12T10:30:00Z"
    }
  ]
}
```

**type 枚举值：**

| 值 | 说明 |
|-----|------|
| agent | 智能体相关 |
| tool | 开源项目相关 |
| document | 文档相关 |
| review | 评价相关 |
| user | 用户相关 |
| auth | 授权码相关 |

---

## 附录

### A. 前端服务层文件对应关系

| 服务层文件 | 对应页面 | 说明 |
|-----------|---------|------|
| services/auth.ts | LoginView.vue | 认证相关 |
| services/agents.ts | AgentsView.vue | 智能体管理 |
| services/tools.ts | ToolsView.vue | 开源项目管理 |
| services/documents.ts | DocumentsView.vue | 文档资料管理 |
| services/reviews.ts | ReviewsView.vue | 用户评价管理 |
| services/authCodes.ts | AuthCodesView.vue | 授权码管理 |
| services/users.ts | UsersView.vue | 用户管理 |
| services/carousel.ts | CarouselView.vue | 轮播文案管理 |
| services/footer.ts | FooterConfigView.vue | 底部配置管理 |

### B. 数据库表设计建议

#### agents 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | VARCHAR(32) | 主键 |
| name | VARCHAR(100) | 智能体名称 |
| api | VARCHAR(500) | API地址 |
| source | VARCHAR(20) | 来源 |
| bot_id | VARCHAR(100) | Coze智能体ID |
| is_visible | BOOLEAN | 是否展示 |
| sort_order | INT | 排序 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### tools 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | VARCHAR(32) | 主键 |
| title | VARCHAR(100) | 标题 |
| description | TEXT | 描述 |
| image | VARCHAR(500) | 图片URL |
| is_visible | BOOLEAN | 是否展示 |
| sort_order | INT | 排序 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### documents 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | VARCHAR(32) | 主键 |
| category | VARCHAR(50) | 分类 |
| title | VARCHAR(200) | 标题 |
| description | TEXT | 描述 |
| date | DATE | 日期 |
| color | VARCHAR(20) | 颜色 |
| is_visible | BOOLEAN | 是否展示 |
| sort_order | INT | 排序 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### reviews 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | VARCHAR(32) | 主键 |
| name | VARCHAR(50) | 用户名 |
| avatar_color | VARCHAR(20) | 头像颜色 |
| rating | INT | 评分(1-5) |
| content | TEXT | 评价内容 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### auth_codes 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | VARCHAR(32) | 主键 |
| description | VARCHAR(200) | 描述 |
| invite_code | VARCHAR(20) | 授权码 |
| status | VARCHAR(20) | 状态 |
| auth_location | VARCHAR(20) | 授权位置 |
| authorized_user | VARCHAR(50) | 授权用户 |
| authorized_at | DATETIME | 授权时间 |
| expire_time | DATETIME | 过期时间 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### users 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | VARCHAR(32) | 主键 |
| username | VARCHAR(50) | 用户名 |
| password | VARCHAR(100) | 密码 |
| role | VARCHAR(20) | 角色 |
| last_login_at | DATETIME | 最后登录时间 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### carousels 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | VARCHAR(32) | 主键 |
| title | VARCHAR(100) | 标题 |
| description | TEXT | 描述 |
| is_visible | BOOLEAN | 是否展示 |
| sort_order | INT | 排序 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### footer_config 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | INT | 主键 |
| logo_url | VARCHAR(500) | Logo URL |
| slogan | TEXT | 标语 |
| updated_at | DATETIME | 更新时间 |

#### footer_links 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | VARCHAR(32) | 主键 |
| title | VARCHAR(100) | 标题 |
| url | VARCHAR(500) | 链接地址 |
| sort_order | INT | 排序 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

**文档版本：** v1.0  
**更新时间：** 2024-02-14

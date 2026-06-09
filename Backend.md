# Cinole Enterprise Backend Technical Document

## 1. Document Information / 文档信息

| Item / 项目 | Content / 内容 |
| --- | --- |
| Project / 项目 | Cinole Enterprise Management System |
| Backend / 后端 | FastAPI |
| Language / 语言 | Python |
| Database Access / 数据库访问 | SQLAlchemy ORM |
| Validation / 数据校验 | Pydantic |
| API Version / API 版本 | v1 |
| Document Date / 文档日期 | 2026-06-09 |

---

## 2. Overview / 后端概览

The backend is a FastAPI application for enterprise master data management. The current implementation focuses on Material and Supplier master data, with a layered structure that separates API routes, schemas, services, repositories, SQLAlchemy models, and database sessions.

后端是基于 FastAPI 的企业管理系统服务端。当前主要实现主数据模块中的物料和供应商管理，并采用分层结构，将 API 路由、请求响应模型、业务服务、数据仓储、SQLAlchemy 模型和数据库会话分开管理。

Current implemented modules:

当前已实现模块：

| Module / 模块 | Status / 状态 |
| --- | --- |
| Material Master / 物料主数据 | Implemented basic CRUD and status update / 已实现基础增查改和状态更新 |
| Supplier Master / 供应商主数据 | Implemented basic CRUD / 已实现基础增查改 |
| Database Session / 数据库会话 | Implemented with SQLAlchemy / 已使用 SQLAlchemy 实现 |
| Request Logging / 请求日志 | Implemented as middleware / 已通过中间件实现 |
| Dev DB Test / 数据库测试接口 | Implemented for development check / 已实现开发期测试接口 |

---

## 3. Technology Stack / 技术栈

| Area / 领域 | Technology / 技术 |
| --- | --- |
| Web framework / Web 框架 | FastAPI |
| ASGI server / ASGI 服务 | Uvicorn |
| ORM / ORM | SQLAlchemy |
| Database driver / 数据库驱动 | psycopg2-binary |
| Settings / 配置 | pydantic-settings |
| Validation / 数据校验 | Pydantic |
| Middleware / 中间件 | Starlette BaseHTTPMiddleware |
| Logging / 日志 | Python logging, RotatingFileHandler |
| Database / 数据库 | PostgreSQL |

Dependency file:

依赖文件：

```text
App/backend/requirements.txt
```

Current dependencies:

当前依赖：

```text
fastapi
uvicorn
pydantic
pydantic-settings
sqlalchemy
psycopg2-binary
```

---

## 4. Directory Structure / 目录结构

```text
App/backend
├── main.py
├── requirements.txt
├── app
│   ├── api
│   │   └── v1
│   │       ├── router.py
│   │       ├── master
│   │       │   ├── material.py
│   │       │   └── supplier.py
│   │       └── system
│   │           └── dev_test
│   │               └── db_test.py
│   ├── core
│   │   ├── config.py
│   │   └── logging.py
│   ├── db
│   │   ├── base.py
│   │   └── session.py
│   ├── middleware
│   │   └── request_log.py
│   ├── models
│   │   └── master
│   │       ├── material_model.py
│   │       └── supplier_model.py
│   ├── repositories
│   │   └── master
│   │       ├── material_repository.py
│   │       └── supplier_repository.py
│   ├── schemas
│   │   └── master
│   │       ├── material
│   │       │   ├── create.py
│   │       │   ├── update.py
│   │       │   ├── response.py
│   │       │   └── query.py
│   │       └── supplier
│   │           ├── create.py
│   │           ├── update.py
│   │           ├── response.py
│   │           └── query.py
│   └── services
│       └── master
│           ├── material_service.py
│           └── supplier_service.py
└── logs
    ├── app.log
    └── error.log
```

### Directory Responsibilities / 目录职责

| Path / 路径 | Responsibility / 职责 |
| --- | --- |
| `main.py` | FastAPI application entry, middleware registration, router mounting. / FastAPI 应用入口，注册中间件和路由。 |
| `app/api/v1` | API route layer with version control. / API 路由层，按版本管理。 |
| `app/core` | Shared configuration and logging. / 公共配置和日志。 |
| `app/db` | SQLAlchemy Base, engine, session factory, and DB dependency. / SQLAlchemy Base、engine、session 工厂和数据库依赖。 |
| `app/middleware` | Request and response middleware. / 请求响应中间件。 |
| `app/models` | SQLAlchemy table mapping models. / SQLAlchemy 数据表映射模型。 |
| `app/repositories` | Direct database query and persistence operations. / 直接数据库查询和持久化操作。 |
| `app/schemas` | Pydantic request, update, response, and query schemas. / Pydantic 请求、更新、响应和查询模型。 |
| `app/services` | Business rules and orchestration. / 业务规则和流程编排。 |
| `logs` | Application and error log output. / 应用日志和错误日志输出。 |

---

## 5. Application Startup / 应用启动

Entry file:

入口文件：

```text
App/backend/main.py
```

Startup behavior:

启动行为：

1. Calls `setup_logging()`.
2. Creates a FastAPI app named `Enterprise Management API`.
3. Adds `RequestLogMiddleware`.
4. Mounts `api_v1_router` under `/api/v1`.
5. Logs startup message on application startup.
6. Exposes root endpoint `/`.

1. 调用 `setup_logging()` 初始化日志。
2. 创建名为 `Enterprise Management API` 的 FastAPI 应用。
3. 注册 `RequestLogMiddleware`。
4. 将 `api_v1_router` 挂载到 `/api/v1`。
5. 应用启动时记录启动日志。
6. 暴露根路径 `/`。

Root endpoint:

根路径接口：

| Method / 方法 | Path / 路径 | Response / 响应 |
| --- | --- | --- |
| `GET` | `/` | `{"message": "FastAPI server is running"}` |

---

## 6. API Routing / API 路由

All current APIs are mounted under:

当前所有接口统一挂载在：

```text
/api/v1
```

Router aggregator:

路由聚合器：

```text
App/backend/app/api/v1/router.py
```

Included routers:

已注册路由：

| Router / 路由 | Prefix / 前缀 | Source / 来源 |
| --- | --- | --- |
| Material / 物料 | `/master/materials` | `app/api/v1/master/material.py` |
| Supplier / 供应商 | `/master/suppliers` | `app/api/v1/master/supplier.py` |
| DB Test / 数据库测试 | `/system/dev-test` | `app/api/v1/system/dev_test/db_test.py` |

### 6.1 Material APIs / 物料接口

Final paths after `/api/v1` mounting:

挂载 `/api/v1` 后的完整路径：

| Method / 方法 | Path / 路径 | Description / 描述 |
| --- | --- | --- |
| `GET` | `/api/v1/master/materials` | List all materials. / 查询物料列表。 |
| `GET` | `/api/v1/master/materials/{material_id}` | Get material by ID. / 根据 ID 查询物料。 |
| `POST` | `/api/v1/master/materials` | Create material and auto-generate material code. / 创建物料并自动生成物料编码。 |
| `PUT` | `/api/v1/master/materials/{material_id}` | Update material fields. / 更新物料字段。 |
| `PATCH` | `/api/v1/master/materials/{material_id}/status` | Update `is_active`. / 更新启用状态。 |

Material code generation:

物料编码生成：

| Category / 分类 | Prefix / 前缀 | Sequence / 序列 | Example / 示例 |
| --- | --- | --- | --- |
| `PRODUCTION` | `PROD` | `master.prod_seq` | `PROD-001` |
| `CONSUMABLE` | `CONS` | `master.cons_seq` | `CONS-001` |
| `STORAGE` | `STOR` | `master.stor_seq` | `STOR-001` |

### 6.2 Supplier APIs / 供应商接口

Final paths after `/api/v1` mounting:

挂载 `/api/v1` 后的完整路径：

| Method / 方法 | Path / 路径 | Description / 描述 |
| --- | --- | --- |
| `GET` | `/api/v1/master/suppliers` | List all suppliers. / 查询供应商列表。 |
| `GET` | `/api/v1/master/suppliers/{supplier_id}` | Get supplier by ID. / 根据 ID 查询供应商。 |
| `POST` | `/api/v1/master/suppliers` | Create supplier and auto-generate supplier code. / 创建供应商并自动生成供应商编码。 |
| `PUT` | `/api/v1/master/suppliers/{supplier_id}` | Update supplier fields. / 更新供应商字段。 |

Supplier code generation:

供应商编码生成：

```text
SUP-0001, SUP-0002, ...
```

The value comes from PostgreSQL sequence:

编码来自 PostgreSQL 序列：

```text
master.supplier_seq
```

### 6.3 Development DB Test APIs / 开发期数据库测试接口

| Method / 方法 | Path / 路径 | Description / 描述 |
| --- | --- | --- |
| `GET` | `/api/v1/system/dev-test/db` | Executes `SELECT current_database()`. / 执行数据库连接测试。 |
| `POST` | `/api/v1/system/dev-test/db-write` | Creates and inserts into `dev_test_logs`. / 测试数据库写入。 |

These endpoints are for development verification and should be disabled, protected, or removed before production deployment.

这些接口用于开发期验证，生产环境前应禁用、加权限保护或移除。

---

## 7. Layered Architecture / 分层架构

Request flow:

请求流程：

```text
Client
  -> FastAPI route
  -> Pydantic schema validation
  -> Service layer
  -> Repository layer
  -> SQLAlchemy model
  -> PostgreSQL
```

中文流程：

```text
客户端
  -> FastAPI 路由
  -> Pydantic 数据校验
  -> Service 业务层
  -> Repository 仓储层
  -> SQLAlchemy 模型
  -> PostgreSQL
```

### Layer Rules / 分层规则

| Layer / 层 | Rule / 规则 |
| --- | --- |
| API | Only handles HTTP input/output and dependency injection. / 只处理 HTTP 输入输出和依赖注入。 |
| Schema | Defines request and response data contracts. / 定义请求和响应数据契约。 |
| Service | Handles business rules, code generation, and errors. / 处理业务规则、编码生成和错误。 |
| Repository | Handles database query and commit operations. / 处理数据库查询和提交。 |
| Model | Maps Python classes to database tables. / 将 Python 类映射到数据库表。 |

---

## 8. Database Configuration / 数据库配置

Configuration file:

配置文件：

```text
App/backend/app/core/config.py
```

Environment file:

环境变量文件：

```text
App/backend/.env
```

Required setting:

必需配置：

```text
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
```

`Settings` uses `pydantic-settings` and loads `.env` with UTF-8 encoding. If `DATABASE_URL` is not provided, the fallback value is:

`Settings` 使用 `pydantic-settings` 并以 UTF-8 读取 `.env`。如果未配置 `DATABASE_URL`，默认值为：

```text
sqlite:///./app.db
```

Current DB session implementation:

当前数据库会话实现：

```text
App/backend/app/db/session.py
```

Important behavior:

重要行为：

* `create_engine(settings.DATABASE_URL, pool_pre_ping=True)`
* `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)`
* `get_db()` yields one SQLAlchemy session per request and closes it after use.

* 使用 `pool_pre_ping=True` 检查连接可用性。
* 使用 `SessionLocal` 创建请求级数据库会话。
* `get_db()` 在请求结束后关闭 session。

---

## 9. Logging / 日志

Logging file:

日志文件：

```text
App/backend/app/core/logging.py
```

Current outputs:

当前输出：

| Output / 输出 | Level / 级别 | File / 文件 |
| --- | --- | --- |
| Console / 控制台 | `INFO` | stdout |
| App log / 应用日志 | `INFO` | `logs/app.log` |
| Error log / 错误日志 | `ERROR` | `logs/error.log` |

Rotation policy:

滚动策略：

| Item / 项目 | Value / 值 |
| --- | --- |
| Max size / 单文件最大大小 | 5 MB |
| Backup count / 备份数量 | 5 |
| Encoding / 编码 | UTF-8 |

Log format:

日志格式：

```text
%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s
```

---

## 10. Request Logging Middleware / 请求日志中间件

Middleware file:

中间件文件：

```text
App/backend/app/middleware/request_log.py
```

Behavior:

行为：

* Generates a UUID request ID.
* Logs request start and completion.
* Logs method, path, client IP, status code, and duration.
* Adds `X-Request-ID` response header.
* Logs exception details when request handling fails.

* 为每个请求生成 UUID 请求 ID。
* 记录请求开始和完成。
* 记录请求方法、路径、客户端 IP、状态码和耗时。
* 在响应头加入 `X-Request-ID`。
* 请求异常时记录异常日志。

---

## 11. Local Development / 本地开发

Install dependencies:

安装依赖：

```bash
cd App/backend
pip install -r requirements.txt
```

Start server:

启动服务：

```bash
cd App/backend
uvicorn main:app --reload
```

Useful URLs:

常用地址：

| URL | Description / 描述 |
| --- | --- |
| `http://127.0.0.1:8000/` | Root health message / 根路径运行状态 |
| `http://127.0.0.1:8000/docs` | Swagger UI / 交互式 API 文档 |
| `http://127.0.0.1:8000/openapi.json` | OpenAPI schema / OpenAPI 结构 |
| `http://127.0.0.1:8000/api/v1/system/dev-test/db` | DB connection test / 数据库连接测试 |

---

## 12. Current Notes / 当前注意事项

* `MaterialQuery` and `SupplierQuery` schemas exist, but list endpoints currently do not accept query filters yet.
* Supplier currently supports create, list, get, and update; there is no dedicated status patch endpoint yet.
* `dev_test` endpoints are useful during development but should not stay publicly exposed in production.
* Existing empty placeholder modules for finance, inventory, procurement, production, and system indicate future expansion areas.

* `MaterialQuery` 和 `SupplierQuery` 已存在，但列表接口当前尚未接收查询筛选参数。
* 供应商当前支持创建、列表、详情和更新，尚未提供单独的状态更新接口。
* `dev_test` 接口适合开发验证，生产环境不应公开暴露。
* finance、inventory、procurement、production、system 等空模块是后续扩展区域。

# Enterprise Management System Backend Technical Specification

## 1. Document Information / 文档信息

| Item / 项目                            | Content / 内容               |
| -------------------------------------- | ---------------------------- |
| Project Name / 项目名称                | Enterprise Management System |
| Backend Framework / 后端框架           | FastAPI                      |
| Language / 开发语言                    | Python                       |
| API Version / API 版本                 | v1                           |
| Current Backend Version / 当前后端版本 | 0.1.0                        |
| Document Date / 文档日期               | 2026-06-07                   |

---

## 2. Backend Overview / 后端概览

### 2.1 Objective / 目标

The backend provides RESTful APIs for the enterprise management system. It is designed around clear module boundaries, versioned APIs, request logging, and reusable schema definitions.

后端为企业管理系统提供 RESTful API 服务。当前结构以清晰的模块边界、API 版本管理、请求日志记录和可复用数据结构定义为核心。

### 2.2 Current Scope / 当前范围

Current implemented backend scope:

* FastAPI application entry point
* Versioned API router: `/api/v1`
* Master data supplier API placeholder
* Request logging middleware
* Rotating file logging foundation
* Pydantic schema package placeholder

当前已实现的后端范围：

* FastAPI 应用入口
* API 版本路由：`/api/v1`
* 主数据供应商 API 占位接口
* 请求日志中间件
* 滚动文件日志基础配置
* Pydantic Schema 包占位结构

---

## 3. Technology Stack / 技术栈

| Area / 领域                | Technology / 技术                   |
| -------------------------- | ----------------------------------- |
| Web Framework / Web 框架   | FastAPI                             |
| ASGI Server / ASGI 服务    | Uvicorn                             |
| Data Validation / 数据校验 | Pydantic                            |
| Middleware / 中间件        | Starlette BaseHTTPMiddleware        |
| Logging / 日志             | Python logging, RotatingFileHandler |

Dependencies are listed in:

依赖文件位置：

```text
App/backend/requirement.txt
```

Current dependency list:

当前依赖：

```text
fastapi
uvicorn
pydantic
```

---

## 4. Directory Structure / 目录结构

```text
App/backend
├── main.py
├── requirement.txt
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── master
│   │           ├── __init__.py
│   │           └── supplier.py
│   ├── core
│   │   ├── __init__.py
│   │   └── logging.py
│   ├── middleware
│   │   ├── __init__.py
│   │   └── request_log.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── supplier.py
│   └── services
└── logs
    └── app.log
```

### 4.1 Directory Responsibilities / 目录职责

| Path / 路径              | Responsibility / 职责                                                                                                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `main.py`              | FastAPI application creation, global middleware registration, API router registration, startup hook, root health endpoint. / 创建 FastAPI 应用，注册全局中间件和 API 路由，定义启动事件与根路径健康接口。 |
| `app/api`              | API layer. Contains route definitions grouped by version and business domain. / API 层，按版本和业务领域组织路由。                                                                                        |
| `app/api/v1/router.py` | API v1 router aggregator. / API v1 路由聚合入口。                                                                                                                                                         |
| `app/api/v1/master`    | Master data API modules. / 主数据相关 API 模块。                                                                                                                                                          |
| `app/core`             | Shared infrastructure code such as logging and future configuration. / 公共基础设施代码，例如日志和后续配置管理。                                                                                         |
| `app/middleware`       | Global request/response middleware. / 全局请求与响应中间件。                                                                                                                                              |
| `app/schemas`          | Pydantic request and response schemas. / Pydantic 请求与响应数据结构。                                                                                                                                    |
| `app/services`         | Reserved service/business logic layer. / 预留服务层与业务逻辑层。                                                                                                                                         |
| `logs`                 | Runtime log output directory. / 运行日志输出目录。                                                                                                                                                        |

---

## 5. Application Entry / 应用入口

Backend entry file:

后端入口文件：

```text
App/backend/main.py
```

Main responsibilities:

* Create the FastAPI application.
* Set the application title to `Enterprise Management API`.
* Set the application version to `0.1.0`.
* Register request logging middleware.
* Mount API v1 routes under `/api/v1`.
* Define startup logging behavior.
* Provide root endpoint `/`.

主要职责：

* 创建 FastAPI 应用实例。
* 设置应用标题为 `Enterprise Management API`。
* 设置应用版本为 `0.1.0`。
* 注册请求日志中间件。
* 将 API v1 路由挂载到 `/api/v1`。
* 定义应用启动日志行为。
* 提供根路径 `/` 接口。

Root endpoint:

根路径接口：

| Method / 方法 | Path / 路径 | Description / 描述                                             |
| ------------- | ----------- | -------------------------------------------------------------- |
| `GET`       | `/`       | Returns basic server running message. / 返回服务运行状态信息。 |

---

## 6. API Routing Design / API 路由设计

### 6.1 Route Versioning / 路由版本管理

All v1 APIs are mounted under:

所有 v1 接口统一挂载在：

```text
/api/v1
```

The version router is defined in:

版本路由定义位置：

```text
App/backend/app/api/v1/router.py
```

This design keeps future API versions isolated, for example:

该设计便于未来隔离不同 API 版本，例如：

```text
/api/v1
/api/v2
```

### 6.2 Current Supplier APIs / 当前供应商接口

Supplier routes are defined in:

供应商路由定义位置：

```text
App/backend/app/api/v1/master/supplier.py
```

Current route prefix:

当前路由前缀：

```text
/master/suppliers
```

After mounting under `/api/v1`, the final API paths are:

挂载到 `/api/v1` 后，最终接口路径为：

| Method / 方法 | Full Path / 完整路径                              | Handler / 处理函数         | Description / 描述                                             |
| ------------- | ------------------------------------------------- | -------------------------- | -------------------------------------------------------------- |
| `GET`       | `/api/v1/master/suppliers`                      | `list_suppliers`         | List suppliers. / 查询供应商列表。                             |
| `GET`       | `/api/v1/master/suppliers/{supplier_id}`        | `get_supplier`           | Get one supplier by ID. / 根据 ID 查询单个供应商。             |
| `POST`      | `/api/v1/master/suppliers`                      | `create_supplier`        | Create supplier placeholder. / 创建供应商占位接口。            |
| `PUT`       | `/api/v1/master/suppliers/{supplier_id}`        | `update_supplier`        | Update supplier placeholder. / 更新供应商占位接口。            |
| `PATCH`     | `/api/v1/master/suppliers/{supplier_id}/status` | `update_supplier_status` | Update supplier status placeholder. / 更新供应商状态占位接口。 |

Current responses are placeholder JSON objects and do not yet connect to database or service-layer logic.

当前响应均为占位 JSON，尚未接入数据库或服务层业务逻辑。

---

## 7. Middleware Design / 中间件设计

### 7.1 Request Logging Middleware / 请求日志中间件

Middleware file:

中间件文件：

```text
App/backend/app/middleware/request_log.py
```

Class:

类名：

```text
RequestLogMiddleware
```

Main behavior:

主要行为：

* Generate a unique `request_id` for each request.
* Record request method, path, and client IP.
* Measure request duration in milliseconds.
* Log request start, completion, and exception events.
* Add `X-Request-ID` response header after successful processing.
* Read client IP from `x-forwarded-for`, then `x-real-ip`, then the direct client address.
* 为每个请求生成唯一 `request_id`。
* 记录请求方法、路径和客户端 IP。
* 统计请求耗时，单位为毫秒。
* 记录请求开始、完成和异常日志。
* 请求成功完成后在响应头加入 `X-Request-ID`。
* 客户端 IP 优先从 `x-forwarded-for` 获取，其次读取 `x-real-ip`，最后使用直接连接地址。

---

## 8. Logging Design / 日志设计

Logging file:

日志文件：

```text
App/backend/app/core/logging.py
```

Current logger name:

当前 logger 名称：

```text
enterprise_api
```

Log output:

日志输出：

```text
logs/app.log
```

Current log format:

当前日志格式：

```text
%(asctime)s | %(levelname)s | %(name)s | %(message)s
```

Current rotation policy:

当前日志滚动策略：

| Item / 项目                    | Value / 值 |
| ------------------------------ | ---------- |
| Max file size / 单文件最大大小 | 5 MB       |
| Backup count / 保留备份数量    | 5          |
| Encoding / 编码                | UTF-8      |

Recommended follow-up:

建议后续补充：

* Define `setup_logging()` to initialize logging safely.
* Define `get_logger(name: str)` to return child loggers consistently.
* Avoid adding duplicate handlers when the app reloads.
* 补充 `setup_logging()`，统一初始化日志。
* 补充 `get_logger(name: str)`，统一获取子 logger。
* 避免应用热重载时重复添加 handler。

---

## 9. Schema Layer / 数据结构层

Schema package:

Schema 包位置：

```text
App/backend/app/schemas
```

Current supplier schema file:

当前供应商 Schema 文件：

```text
App/backend/app/schemas/supplier.py
```

Current status:

当前状态：

* The schema package exists.
* Supplier schema file exists.
* Supplier request/response models are not yet defined.
* Schema 包已建立。
* 供应商 Schema 文件已建立。
* 供应商请求与响应模型尚未定义。

Recommended supplier schema examples:

建议后续供应商 Schema 拆分：

| Schema / 模型            | Purpose / 用途                                 |
| ------------------------ | ---------------------------------------------- |
| `SupplierBase`         | Shared fields. / 公共字段。                    |
| `SupplierCreate`       | Create request body. / 创建请求体。            |
| `SupplierUpdate`       | Update request body. / 更新请求体。            |
| `SupplierStatusUpdate` | Status update request body. / 状态更新请求体。 |
| `SupplierResponse`     | API response body. / API 响应体。              |

---

## 10. Service Layer / 服务层

Service directory:

服务层目录：

```text
App/backend/app/services
```

Current status:

当前状态：

* Directory exists.
* Business services are not yet implemented.
* 目录已建立。
* 业务服务尚未实现。

Recommended responsibility:

建议职责：

* Keep API route functions thin.
* Move business rules into service modules.
* Keep database access outside route functions.
* Make services reusable by different API endpoints.
* 保持 API 路由函数简洁。
* 将业务规则放入 service 模块。
* 避免在路由函数中直接编写数据库访问逻辑。
* 让服务逻辑可被多个接口复用。

Recommended future module:

建议后续模块：

```text
App/backend/app/services/supplier_service.py
```

---

## 11. Runtime Flow / 运行流程

Request lifecycle:

请求生命周期：

```text
Client
  ↓
FastAPI app in main.py
  ↓
RequestLogMiddleware
  ↓
/api/v1 router
  ↓
Business domain router, for example /master/suppliers
  ↓
Route handler
  ↓
JSON response with X-Request-ID header
```

中文说明：

```text
客户端
  ↓
main.py 中的 FastAPI 应用
  ↓
RequestLogMiddleware 请求日志中间件
  ↓
/api/v1 版本路由
  ↓
业务域路由，例如 /master/suppliers
  ↓
路由处理函数
  ↓
返回 JSON 响应，并附带 X-Request-ID 响应头
```

---

## 12. Local Development / 本地开发

### 12.1 Install Dependencies / 安装依赖

Run from backend directory:

在后端目录下执行：

```bash
cd App/backend
pip install -r requirement.txt
```

### 12.2 Start Development Server / 启动开发服务

```bash
cd App/backend
uvicorn main:app --reload
```

Default local address:

默认本地地址：

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

FastAPI 交互式接口文档：

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

OpenAPI JSON 地址：

```text
http://127.0.0.1:8000/openapi.json
```

---

## 13. Current Known Issues / 当前已知问题

### 13.1 Router Import Mismatch / 路由导入文件名不一致

Current file:

当前文件：

```text
App/backend/app/api/v1/master/supplier.py
```

Current import in `App/backend/app/api/v1/router.py`:

`App/backend/app/api/v1/router.py` 当前导入：

```python
from app.api.v1.master.suppliers import router as suppliers_router
```

Issue:

问题：

* The import expects `suppliers.py`, but the actual file is `supplier.py`.
* This will cause `ModuleNotFoundError` when starting the application.
* 导入语句期望文件名为 `suppliers.py`，但实际文件名为 `supplier.py`。
* 启动应用时会导致 `ModuleNotFoundError`。

Recommended fix:

建议修复方式：

```python
from app.api.v1.master.supplier import router as suppliers_router
```

Alternative:

或者将文件重命名为：

```text
suppliers.py
```

### 13.2 Missing Logging Helper Functions / 日志辅助函数缺失

Current imports in `main.py` and middleware:

`main.py` 和中间件中当前导入：

```python
from app.core.logging import setup_logging, get_logger
```

Issue:

问题：

* `app/core/logging.py` currently configures a logger directly.
* `setup_logging()` and `get_logger()` are referenced but not defined.
* This will cause `ImportError` when starting the application.
* `app/core/logging.py` 当前直接配置 logger。
* `setup_logging()` 和 `get_logger()` 被引用，但尚未定义。
* 启动应用时会导致 `ImportError`。

Recommended fix:

建议修复：

* Add `setup_logging()` to initialize handlers.
* Add `get_logger(name: str)` to return loggers consistently.
* Keep logger setup idempotent to prevent duplicate logs during reload.
* 添加 `setup_logging()`，用于初始化 handler。
* 添加 `get_logger(name: str)`，用于统一返回 logger。
* 保持日志初始化幂等，避免热重载时重复输出日志。

---

## 14. Recommended Backend Evolution / 后续演进建议

Recommended next steps:

建议下一步：

1. Fix router import and logging helper functions.
2. Define Pydantic schemas for supplier create, update, status update, and response.
3. Add service layer module for supplier business logic.
4. Add database connection layer, preferably under `app/db`.
5. Add repository or DAO layer if database access becomes complex.
6. Add environment-based configuration management.
7. Add automated tests for routers, middleware, and services.
8. Add unified response and error handling conventions.
9. 修复路由导入和日志辅助函数。
10. 定义供应商创建、更新、状态更新和响应相关 Pydantic Schema。
11. 添加供应商业务服务层模块。
12. 添加数据库连接层，建议放在 `app/db`。
13. 如果数据库访问复杂，增加 Repository 或 DAO 层。
14. 增加基于环境变量的配置管理。
15. 为路由、中间件和服务层添加自动化测试。
16. 建立统一响应格式和异常处理规范。

Recommended future structure:

建议未来结构：

```text
App/backend/app
├── api
│   └── v1
│       ├── router.py
│       └── master
│           └── supplier.py
├── core
│   ├── config.py
│   └── logging.py
├── db
│   ├── session.py
│   └── base.py
├── middleware
│   └── request_log.py
├── models
│   └── supplier.py
├── repositories
│   └── supplier_repository.py
├── schemas
│   └── supplier.py
└── services
    └── supplier_service.py
```

---

## 15. Naming Conventions / 命名规范

### 15.1 API Routes / API 路由

English:

* Use plural nouns for resource paths, for example `/suppliers`.
* Use lowercase path segments.
* Use HTTP methods to express actions where possible.
* Use action suffixes only when the operation is not a standard CRUD action, for example `/status`.

中文：

* 资源路径使用复数名词，例如 `/suppliers`。
* 路径片段使用小写。
* 尽量使用 HTTP 方法表达动作。
* 只有非标准 CRUD 操作才使用动作后缀，例如 `/status`。

### 15.2 Python Modules / Python 模块

English:

* Use lowercase module names.
* Keep route modules aligned with resource names.
* Keep schema names explicit, for example `SupplierCreate`.

中文：

* 模块名使用小写。
* 路由模块名与资源名保持一致。
* Schema 名称表达具体用途，例如 `SupplierCreate`。

---

## 16. Summary / 总结

The current backend already has a clean FastAPI foundation: application entry, versioned routing, middleware, logging, schema package, and reserved service layer. The immediate priority is to fix the router import mismatch and complete the logging helper functions so the application can start reliably. After that, supplier schemas, service logic, and database integration can be added incrementally.

当前后端已经具备清晰的 FastAPI 基础结构：应用入口、版本化路由、中间件、日志、Schema 包和预留服务层。当前最优先的工作是修复路由导入不一致以及补全日志辅助函数，确保应用可以稳定启动。之后可以逐步补充供应商 Schema、服务层业务逻辑和数据库集成。

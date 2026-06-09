# Cinole Enterprise Database Technical Document

## 1. Document Information / 文档信息

| Item / 项目 | Content / 内容 |
| --- | --- |
| Project / 项目 | Cinole Enterprise Management System |
| Database / 数据库 | PostgreSQL |
| Schema File / 建表脚本 | `schema.sql` |
| Backend ORM / 后端 ORM | SQLAlchemy |
| Current Phase / 当前阶段 | Master Data Foundation / 主数据基础 |
| Document Date / 文档日期 | 2026-06-09 |

---

## 2. Overview / 数据库概览

The current database script builds the master data foundation for the system. It creates the `master` schema, material sequences, supplier sequence, and two master data tables: `master.materials` and `master.suppliers`.

当前数据库脚本用于建立系统主数据基础。脚本创建 `master` schema、物料编码序列、供应商编码序列，以及两张主数据表：`master.materials` 和 `master.suppliers`。

Current implemented database objects:

当前已实现数据库对象：

| Type / 类型 | Name / 名称 | Purpose / 用途 |
| --- | --- | --- |
| Schema / Schema | `master` | Master data namespace / 主数据命名空间 |
| Table / 表 | `master.materials` | Material master data / 物料主数据 |
| Table / 表 | `master.suppliers` | Supplier master data / 供应商主数据 |
| Sequence / 序列 | `master.prod_seq` | Production material code number / 生产类物料编码序号 |
| Sequence / 序列 | `master.cons_seq` | Consumable material code number / 消耗品物料编码序号 |
| Sequence / 序列 | `master.stor_seq` | Storage material code number / 仓储类物料编码序号 |
| Sequence / 序列 | `master.supplier_seq` | Supplier code number / 供应商编码序号 |

---

## 3. Schema Design / Schema 设计

Current schema:

当前 schema：

```sql
CREATE SCHEMA IF NOT EXISTS master;
```

Design rule:

设计规则：

* Master data tables are stored under `master`.
* Table names use plural nouns: `materials`, `suppliers`.
* Primary keys use `id BIGSERIAL PRIMARY KEY`.
* Business codes use unique varchar fields, such as `material_code` and `supplier_code`.
* Timestamps use `created_at` and `updated_at`.

* 主数据表统一放在 `master` 下。
* 表名使用复数名词：`materials`、`suppliers`。
* 主键统一使用 `id BIGSERIAL PRIMARY KEY`。
* 业务编码使用唯一 varchar 字段，例如 `material_code` 和 `supplier_code`。
* 时间字段统一使用 `created_at` 和 `updated_at`。

---

## 4. Sequences / 序列

### 4.1 Material Sequences / 物料序列

```sql
CREATE SEQUENCE IF NOT EXISTS master.prod_seq START 1;
CREATE SEQUENCE IF NOT EXISTS master.cons_seq START 1;
CREATE SEQUENCE IF NOT EXISTS master.stor_seq START 1;
```

Backend code generation:

后端编码生成：

| Category / 分类 | Sequence / 序列 | Code Prefix / 编码前缀 | Example / 示例 |
| --- | --- | --- | --- |
| `PRODUCTION` | `master.prod_seq` | `PROD` | `PROD-001` |
| `CONSUMABLE` | `master.cons_seq` | `CONS` | `CONS-001` |
| `STORAGE` | `master.stor_seq` | `STOR` | `STOR-001` |

### 4.2 Supplier Sequence / 供应商序列

```sql
CREATE SEQUENCE IF NOT EXISTS master.supplier_seq START 1;
```

Backend code generation:

后端编码生成：

| Sequence / 序列 | Code Format / 编码格式 | Example / 示例 |
| --- | --- | --- |
| `master.supplier_seq` | `SUP-{number:04d}` | `SUP-0001` |

---

## 5. Table: master.materials / 表：master.materials

Purpose:

用途：

Stores material master data, including material code, names, category, type, base unit, specification, status, remarks, and timestamps.

存储物料主数据，包括物料编码、名称、分类、类型、基本计量单位、规格、状态、备注和时间戳。

### 5.1 Columns / 字段

| Column / 字段 | Type / 类型 | Required / 必填 | Unique / 唯一 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- | --- |
| `id` | `BIGSERIAL` | Yes | Yes | Auto increment | Primary key / 主键 |
| `material_code` | `VARCHAR(50)` | Yes | Yes | Backend generated | Material business code / 物料业务编码 |
| `material_name_cn` | `VARCHAR(200)` | Yes | No | - | Chinese material name / 物料中文名称 |
| `material_name_en` | `VARCHAR(200)` | No | No | `NULL` | English material name / 物料英文名称 |
| `material_category_code` | `VARCHAR(50)` | Yes | No | - | Category code / 物料分类编码 |
| `material_type_code` | `VARCHAR(50)` | Yes | No | - | Type code / 物料类型编码 |
| `base_uom_code` | `VARCHAR(20)` | Yes | No | - | Base unit of measure / 基本计量单位 |
| `specification` | `VARCHAR(200)` | No | No | `NULL` | Specification / 规格型号 |
| `is_active` | `BOOLEAN` | Yes | No | `TRUE` | Active status / 是否启用 |
| `remark` | `TEXT` | No | No | `NULL` | Remarks / 备注 |
| `created_at` | `TIMESTAMP` | Yes | No | `CURRENT_TIMESTAMP` | Created time / 创建时间 |
| `updated_at` | `TIMESTAMP` | Yes | No | `CURRENT_TIMESTAMP` | Updated time / 更新时间 |

### 5.2 Indexes / 索引

```sql
CREATE INDEX IF NOT EXISTS idx_materials_name_cn
ON master.materials (material_name_cn);

CREATE INDEX IF NOT EXISTS idx_materials_category_code
ON master.materials (material_category_code);

CREATE INDEX IF NOT EXISTS idx_materials_type_code
ON master.materials (material_type_code);

CREATE INDEX IF NOT EXISTS idx_materials_is_active
ON master.materials (is_active);
```

Index purpose:

索引用途：

| Index / 索引 | Purpose / 用途 |
| --- | --- |
| `idx_materials_name_cn` | Search or sort by Chinese name / 按中文名称查询或排序 |
| `idx_materials_category_code` | Filter by material category / 按物料分类筛选 |
| `idx_materials_type_code` | Filter by material type / 按物料类型筛选 |
| `idx_materials_is_active` | Filter active or inactive materials / 按启用状态筛选 |

---

## 6. Table: master.suppliers / 表：master.suppliers

Purpose:

用途：

Stores supplier identity, contact, tax, invoice, bank, payment, legal, status, remarks, and timestamps in one table.

在一张表中存储供应商基础身份、联系人、税务、开票、银行付款、法务授权、状态、备注和时间戳。

### 6.1 Columns / 字段

| Column / 字段 | Type / 类型 | Required / 必填 | Unique / 唯一 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- | --- |
| `id` | `BIGSERIAL` | Yes | Yes | Auto increment | Primary key / 主键 |
| `supplier_code` | `VARCHAR(50)` | Yes | Yes | Backend generated | Supplier business code / 供应商业务编码 |
| `supplier_name_cn` | `VARCHAR(200)` | Yes | No | - | Chinese supplier name / 供应商中文名称 |
| `supplier_name_en` | `VARCHAR(200)` | No | No | `NULL` | English supplier name / 供应商英文名称 |
| `supplier_short_code` | `VARCHAR(50)` | No | No | `NULL` | Supplier short code / 供应商简称编码 |
| `supplier_type_code` | `VARCHAR(50)` | No | No | `NULL` | Supplier type code / 供应商类型编码 |
| `contact_name` | `VARCHAR(100)` | No | No | `NULL` | Contact person / 联系人 |
| `position_title` | `VARCHAR(100)` | No | No | `NULL` | Position title / 职位 |
| `phone` | `VARCHAR(50)` | No | No | `NULL` | Contact phone / 联系电话 |
| `email` | `VARCHAR(100)` | No | No | `NULL` | Email / 邮箱 |
| `tax_registration_no` | `VARCHAR(100)` | No | No | `NULL` | Tax registration number / 税号 |
| `invoice_company_name` | `VARCHAR(200)` | No | No | `NULL` | Invoice company name / 开票公司名称 |
| `invoice_address` | `TEXT` | No | No | `NULL` | Invoice address / 开票地址 |
| `invoice_phone` | `VARCHAR(50)` | No | No | `NULL` | Invoice phone / 开票电话 |
| `bank_name` | `VARCHAR(200)` | No | No | `NULL` | Bank name / 开户银行 |
| `bank_account_name` | `VARCHAR(200)` | No | No | `NULL` | Bank account holder / 开户名称 |
| `bank_account_no` | `VARCHAR(100)` | No | No | `NULL` | Bank account number / 银行账号 |
| `currency_code` | `VARCHAR(20)` | Yes | No | `CNY` | Settlement currency / 结算币种 |
| `entrusted_person_name` | `VARCHAR(100)` | No | No | `NULL` | Entrusted person / 委托人 |
| `legal_representative` | `VARCHAR(100)` | No | No | `NULL` | Legal representative / 法定代表人 |
| `is_active` | `BOOLEAN` | Yes | No | `TRUE` | Active status / 是否启用 |
| `remark` | `TEXT` | No | No | `NULL` | Remarks / 备注 |
| `created_at` | `TIMESTAMP` | Yes | No | `CURRENT_TIMESTAMP` | Created time / 创建时间 |
| `updated_at` | `TIMESTAMP` | Yes | No | `CURRENT_TIMESTAMP` | Updated time / 更新时间 |

### 6.2 Indexes / 索引

```sql
CREATE INDEX IF NOT EXISTS idx_suppliers_name_cn
ON master.suppliers (supplier_name_cn);

CREATE INDEX IF NOT EXISTS idx_suppliers_short_code
ON master.suppliers (supplier_short_code);

CREATE INDEX IF NOT EXISTS idx_suppliers_type_code
ON master.suppliers (supplier_type_code);

CREATE INDEX IF NOT EXISTS idx_suppliers_is_active
ON master.suppliers (is_active);
```

Index purpose:

索引用途：

| Index / 索引 | Purpose / 用途 |
| --- | --- |
| `idx_suppliers_name_cn` | Search or sort by Chinese supplier name / 按供应商中文名称查询或排序 |
| `idx_suppliers_short_code` | Search by short code / 按简称编码查询 |
| `idx_suppliers_type_code` | Filter by supplier type / 按供应商类型筛选 |
| `idx_suppliers_is_active` | Filter active or inactive suppliers / 按启用状态筛选 |

---

## 7. ORM Mapping / ORM 映射

SQLAlchemy models:

SQLAlchemy 模型：

| Database Table / 数据表 | ORM Model / ORM 模型 | File / 文件 |
| --- | --- | --- |
| `master.materials` | `Material` | `App/backend/app/models/master/material_model.py` |
| `master.suppliers` | `Supplier` | `App/backend/app/models/master/supplier_model.py` |

Both models use:

两个模型都使用：

```python
__table_args__ = {"schema": "master"}
```

This makes SQLAlchemy read and write tables under the PostgreSQL `master` schema.

这会让 SQLAlchemy 读写 PostgreSQL 的 `master` schema 下的数据表。

---

## 8. Backend Data Flow / 后端数据流

Material create flow:

物料创建流程：

```text
POST /api/v1/master/materials
  -> MaterialCreate
  -> material_service.generate_material_code()
  -> material_repository.get_next_material_sequence()
  -> INSERT master.materials
```

Supplier create flow:

供应商创建流程：

```text
POST /api/v1/master/suppliers
  -> SupplierCreate
  -> supplier_service.generate_supplier_code()
  -> nextval('master.supplier_seq')
  -> INSERT master.suppliers
```

---

## 9. Current Limitations / 当前限制

* `updated_at` has a default value, but `schema.sql` does not define a database trigger to automatically refresh it on every update. SQLAlchemy models use `onupdate=func.now()` when updates go through ORM.
* There are no foreign keys yet because only master data foundation tables are currently implemented.
* Query schemas exist in backend code, but list filtering is not implemented in current API routes.
* `dev_test_logs` is created by the development test endpoint, not by `schema.sql`.

* `updated_at` 有默认值，但 `schema.sql` 尚未定义数据库触发器自动更新时间。通过 ORM 更新时，模型使用 `onupdate=func.now()`。
* 当前只实现主数据基础表，尚未定义外键。
* 后端已有查询 Schema，但当前列表接口尚未实现筛选。
* `dev_test_logs` 由开发测试接口动态创建，不属于 `schema.sql` 的正式表结构。

---

## 10. Recommended Next Steps / 后续建议

1. Add database migration management, such as Alembic.
2. Add database-level `updated_at` trigger if non-ORM updates are expected.
3. Add seed data for common material categories, material types, units, supplier types, and currencies.
4. Implement query filters for material and supplier list endpoints.
5. Add constraints or reference tables for code fields such as `material_category_code`, `material_type_code`, `base_uom_code`, `supplier_type_code`, and `currency_code`.
6. Split supplier contact, bank, and invoice information into child tables if historical records or multiple records are required later.

1. 增加数据库迁移工具，例如 Alembic。
2. 如果存在非 ORM 更新，建议增加数据库级 `updated_at` 触发器。
3. 增加物料分类、物料类型、单位、供应商类型、币种等基础字典种子数据。
4. 为物料和供应商列表接口实现查询筛选。
5. 为 `material_category_code`、`material_type_code`、`base_uom_code`、`supplier_type_code`、`currency_code` 等编码字段增加约束或字典表。
6. 如果后续需要历史记录或多联系人/多账户，可将供应商联系人、银行、开票信息拆分为子表。

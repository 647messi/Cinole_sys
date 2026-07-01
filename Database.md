# Cinole Enterprise Database Technical Document

## 1. Document Information / 文档信息

| Item / 项目 | Content / 内容 |
| --- | --- |
| Project / 项目 | Cinole Enterprise Management System |
| Database / 数据库 | PostgreSQL |
| Schema File / 建表脚本 | `schema.sql` |
| Backend ORM / 后端 ORM | SQLAlchemy |
| Current Phase / 当前阶段 | Master Data Foundation / 主数据基础 |
| Document Date / 文档日期 | 2026-06-30 |

---

## 2. Overview / 数据库概览

The current database script builds the master data foundation for the system. It creates the `master` schema, material sequences, supplier sequence, the material master table, and supplier-related master tables for supplier identity, origin addresses, and financial information.

当前数据库脚本用于建立系统主数据基础。脚本创建 `master` schema、物料编码序列、供应商编码序列、物料主数据表，以及供应商基础信息、产地地址、财务信息相关主数据表。

Current implemented database objects:

当前已实现数据库对象：

| Type / 类型 | Name / 名称 | Purpose / 用途 |
| --- | --- | --- |
| Schema / Schema | `master` | Master data namespace / 主数据命名空间 |
| Table / 表 | `master.materials` | Material master data / 物料主数据 |
| Table / 表 | `master.suppliers` | Supplier identity and primary contact data / 供应商基础身份和主要联系人信息 |
| Table / 表 | `master.supplier_origin_addresses` | Supplier origin address records / 供应商产地地址记录 |
| Table / 表 | `master.supplier_finance_infos` | Supplier invoice, tax, and bank settlement records / 供应商开票、税务和银行结算信息 |
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
* Table names use plural nouns: `materials`, `suppliers`, `supplier_origin_addresses`, `supplier_finance_infos`.
* Primary keys use `id BIGSERIAL PRIMARY KEY`.
* Business codes use unique varchar fields, such as `material_code` and `supplier_id`.
* Supplier child tables reference `master.suppliers(id)` with `ON DELETE CASCADE`.
* Tables that need audit timestamps use `created_at` and `updated_at`.

* 主数据表统一放在 `master` 下。
* 表名使用复数名词：`materials`、`suppliers`、`supplier_origin_addresses`、`supplier_finance_infos`。
* 主键统一使用 `id BIGSERIAL PRIMARY KEY`。
* 业务编码使用唯一 varchar 字段，例如 `material_code` 和 `supplier_id`。
* 供应商子表通过外键引用 `master.suppliers(id)`，并使用 `ON DELETE CASCADE`。
* 需要审计时间的表使用 `created_at` 和 `updated_at`。

---

## 4. Sequences / 序列

### 4.1 Material Sequences / 物料序列

```sql
CREATE SEQUENCE IF NOT EXISTS master.prod_seq START 1;
CREATE SEQUENCE IF NOT EXISTS master.cons_seq START 1;
CREATE SEQUENCE IF NOT EXISTS master.stor_seq START 1;
```

Current usage:

当前用途：

These sequences are still defined in `schema.sql`, but the current `master.materials` table expects `material_code` to be provided by the create request.

这些序列仍在 `schema.sql` 中定义，但当前 `master.materials` 表要求创建请求直接提供 `material_code`。

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

Stores material master data, including material code, names, base unit, status, and remarks.

存储物料主数据，包括物料编码、名称、基本计量单位、状态和备注。

### 5.1 Columns / 字段

| Column / 字段 | Type / 类型 | Required / 必填 | Unique / 唯一 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- | --- |
| `id` | `BIGSERIAL` | Yes | Yes | Auto increment | Primary key / 主键 |
| `material_code` | `VARCHAR(50)` | Yes | Yes | Request provided | Material business code / 物料业务编码 |
| `material_name_cn` | `VARCHAR(200)` | Yes | No | - | Chinese material name / 物料中文名称 |
| `material_name_en` | `VARCHAR(200)` | No | No | `NULL` | English material name / 物料英文名称 |
| `base_uom_code` | `VARCHAR(20)` | Yes | No | - | Base unit of measure / 基本计量单位 |
| `is_active` | `BOOLEAN` | Yes | No | `TRUE` | Active status / 是否启用 |
| `remark` | `TEXT` | No | No | `NULL` | Remarks / 备注 |

### 5.2 Indexes / 索引

```sql
CREATE INDEX IF NOT EXISTS idx_materials_name_cn
ON master.materials (material_name_cn);

CREATE INDEX IF NOT EXISTS idx_materials_is_active
ON master.materials (is_active);
```

Index purpose:

索引用途：

| Index / 索引 | Purpose / 用途 |
| --- | --- |
| `idx_materials_name_cn` | Search or sort by Chinese name / 按中文名称查询或排序 |
| `idx_materials_is_active` | Filter active or inactive materials / 按启用状态筛选 |

---

## 6. Table: master.suppliers / 表：master.suppliers

Purpose:

用途：

Stores supplier identity, primary contact, status, remarks, and timestamps. Tax, invoice, bank, payment, and origin address information is stored in supplier child tables.

存储供应商基础身份、主要联系人、状态、备注和时间戳。税务、开票、银行付款和产地地址信息存储在供应商子表中。

### 6.1 Columns / 字段

| Column / 字段 | Type / 类型 | Required / 必填 | Unique / 唯一 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- | --- |
| `id` | `BIGSERIAL` | Yes | Yes | Auto increment | Primary key / 主键 |
| `supplier_id` | `VARCHAR(50)` | Yes | Yes | Backend generated | Supplier business ID / 供应商业务 ID |
| `supplier_name_cn` | `VARCHAR(200)` | Yes | No | - | Chinese supplier name / 供应商中文名称 |
| `supplier_name_en` | `VARCHAR(200)` | No | No | `NULL` | English supplier name / 供应商英文名称 |
| `supplier_short_code` | `VARCHAR(50)` | No | No | `NULL` | Supplier short code / 供应商简称编码 |
| `supplier_type_code` | `VARCHAR(50)` | No | No | `NULL` | Supplier type code / 供应商类型编码 |
| `contact_name` | `VARCHAR(100)` | No | No | `NULL` | Contact person / 联系人 |
| `phone` | `VARCHAR(50)` | No | No | `NULL` | Contact phone / 联系电话 |
| `email` | `VARCHAR(100)` | No | No | `NULL` | Email / 邮箱 |
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

## 7. Table: master.supplier_origin_addresses / 表：master.supplier_origin_addresses

Purpose:

用途：

Stores one or more origin addresses for a supplier. Each supplier can have at most one default origin address.

存储供应商的一个或多个产地地址。每个供应商最多只能有一个默认产地地址。

### 7.1 Columns / 字段

| Column / 字段 | Type / 类型 | Required / 必填 | Unique / 唯一 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- | --- |
| `id` | `BIGSERIAL` | Yes | Yes | Auto increment | Primary key / 主键 |
| `supplier_id` | `BIGINT` | Yes | No | - | FK to `master.suppliers(id)` / 供应商外键 |
| `origin_address` | `TEXT` | Yes | No | - | Full origin address / 完整产地地址 |
| `country` | `VARCHAR(100)` | No | No | `NULL` | Country / 国家 |
| `province` | `VARCHAR(100)` | No | No | `NULL` | Province or state / 省份或州 |
| `city` | `VARCHAR(100)` | No | No | `NULL` | City / 城市 |
| `district` | `VARCHAR(100)` | No | No | `NULL` | District / 区县 |
| `postal_code` | `VARCHAR(50)` | No | No | `NULL` | Postal code / 邮编 |
| `detailed_address` | `VARCHAR(200)` | No | No | `NULL` | Detailed street address / 详细地址 |
| `is_default` | `BOOLEAN` | Yes | Per supplier | `FALSE` | Default address flag / 默认地址标记 |
| `is_active` | `BOOLEAN` | Yes | No | `TRUE` | Active status / 是否启用 |
| `remark` | `TEXT` | No | No | `NULL` | Remarks / 备注 |
| `created_at` | `TIMESTAMP` | Yes | No | `CURRENT_TIMESTAMP` | Created time / 创建时间 |
| `updated_at` | `TIMESTAMP` | Yes | No | `CURRENT_TIMESTAMP` | Updated time / 更新时间 |

### 7.2 Constraints and Indexes / 约束和索引

```sql
supplier_id BIGINT NOT NULL REFERENCES master.suppliers(id) ON DELETE CASCADE

CREATE INDEX IF NOT EXISTS idx_supplier_origin_addresses_supplier_id
ON master.supplier_origin_addresses (supplier_id);

CREATE INDEX IF NOT EXISTS idx_supplier_origin_addresses_is_active
ON master.supplier_origin_addresses (is_active);

CREATE UNIQUE INDEX IF NOT EXISTS uq_supplier_origin_default
ON master.supplier_origin_addresses (supplier_id)
WHERE is_default = TRUE;
```

| Constraint or Index / 约束或索引 | Purpose / 用途 |
| --- | --- |
| FK `supplier_id -> master.suppliers(id)` | Delete child addresses when supplier is deleted / 删除供应商时级联删除地址 |
| `idx_supplier_origin_addresses_supplier_id` | Find addresses by supplier / 按供应商查询地址 |
| `idx_supplier_origin_addresses_is_active` | Filter active or inactive addresses / 按启用状态筛选地址 |
| `uq_supplier_origin_default` | Allow only one default origin address per supplier / 每个供应商只允许一个默认产地地址 |

---

## 8. Table: master.supplier_finance_infos / 表：master.supplier_finance_infos

Purpose:

用途：

Stores invoice, tax, bank, payment, status, remarks, and timestamps for suppliers. Each supplier may have multiple finance records.

存储供应商开票、税务、银行付款、状态、备注和时间戳。每个供应商可以有多条财务信息记录。

### 8.1 Columns / 字段

| Column / 字段 | Type / 类型 | Required / 必填 | Unique / 唯一 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- | --- |
| `id` | `BIGSERIAL` | Yes | Yes | Auto increment | Primary key / 主键 |
| `supplier_id` | `BIGINT` | Yes | No | - | FK to `master.suppliers(id)` / 供应商外键 |
| `invoice_company_name` | `VARCHAR(200)` | No | No | `NULL` | Invoice company name / 开票公司名称 |
| `tax_registration_no` | `VARCHAR(100)` | No | No | `NULL` | Tax registration number / 税号 |
| `invoice_address` | `TEXT` | No | No | `NULL` | Invoice address / 开票地址 |
| `invoice_phone` | `VARCHAR(50)` | No | No | `NULL` | Invoice phone / 开票电话 |
| `bank_name` | `VARCHAR(200)` | No | No | `NULL` | Bank name / 开户银行 |
| `bank_account_name` | `VARCHAR(200)` | No | No | `NULL` | Bank account holder / 开户名称 |
| `bank_account_no` | `VARCHAR(100)` | No | No | `NULL` | Bank account number / 银行账号 |
| `currency_code` | `VARCHAR(20)` | Yes | No | `CNY` | Settlement currency / 结算币种 |
| `is_default` | `BOOLEAN` | Yes | No | `FALSE` | Default finance record flag / 默认财务信息标记 |
| `is_active` | `BOOLEAN` | Yes | No | `TRUE` | Active status / 是否启用 |
| `remark` | `TEXT` | No | No | `NULL` | Remarks / 备注 |
| `created_at` | `TIMESTAMP` | Yes | No | `CURRENT_TIMESTAMP` | Created time / 创建时间 |
| `updated_at` | `TIMESTAMP` | Yes | No | `CURRENT_TIMESTAMP` | Updated time / 更新时间 |

### 8.2 Constraints and Indexes / 约束和索引

```sql
supplier_id BIGINT NOT NULL REFERENCES master.suppliers(id) ON DELETE CASCADE
```

| Constraint or Index / 约束或索引 | Purpose / 用途 |
| --- | --- |
| FK `supplier_id -> master.suppliers(id)` | Delete child finance records when supplier is deleted / 删除供应商时级联删除财务信息 |

Note: `schema.sql` currently does not define indexes for `master.supplier_finance_infos`.

备注：当前 `schema.sql` 尚未为 `master.supplier_finance_infos` 定义索引。

---

## 9. ORM Mapping / ORM 映射

SQLAlchemy models:

SQLAlchemy 模型：

| Database Table / 数据表 | ORM Model / ORM 模型 | File / 文件 |
| --- | --- | --- |
| `master.materials` | `Material` | `App/backend/app/models/master/raw_material_dict_model.py` |
| `master.suppliers` | `Supplier` | `App/backend/app/models/master/supplier_model.py` |
| `master.supplier_origin_addresses` | `SupplierOriginAddress` | `App/backend/app/models/master/supplier_model.py` |
| `master.supplier_finance_infos` | `SupplierFinanceInfo` | `App/backend/app/models/master/supplier_model.py` |

Both models use:

两个模型都使用：

```python
__table_args__ = {"schema": "master"}
```

This makes SQLAlchemy read and write tables under the PostgreSQL `master` schema.

这会让 SQLAlchemy 读写 PostgreSQL 的 `master` schema 下的数据表。

---

Supplier relationships:

供应商关系：

| Parent / 父模型 | Child / 子模型 | Relationship / 关系 |
| --- | --- | --- |
| `Supplier` | `SupplierOriginAddress` | `Supplier.origin_addresses` with cascade delete / `Supplier.origin_addresses`，级联删除 |
| `Supplier` | `SupplierFinanceInfo` | `Supplier.finance_infos` with cascade delete / `Supplier.finance_infos`，级联删除 |

---

## 10. Backend Data Flow / 后端数据流

Material create flow:

物料创建流程：

```text
POST /api/v1/master/raw_material_dict
  -> MaterialCreate
  -> request-provided material_code
  -> INSERT master.materials
```

Supplier create flow:

供应商创建流程：

```text
POST /api/v1/master/suppliers
  -> SupplierCreate
  -> supplier_service.generate_supplier_id()
  -> nextval('master.supplier_seq')
  -> INSERT master.suppliers
```

---

## 11. Current Limitations / 当前限制

* Some tables have `updated_at` default values, but `schema.sql` does not define a database trigger to automatically refresh them on every update. SQLAlchemy models use `onupdate=func.now()` for mapped timestamp fields when updates go through ORM.
* Supplier origin address and finance tables are mapped in ORM, but dedicated CRUD APIs for these child tables are not implemented yet.
* `master.supplier_finance_infos` currently has a foreign key but no supporting indexes in `schema.sql`.
* Query schemas exist in backend code, but list filtering is not implemented in current API routes.
* `dev_test_logs` is created by the development test endpoint, not by `schema.sql`.

* 部分表有 `updated_at` 默认值，但 `schema.sql` 尚未定义数据库触发器自动更新时间。通过 ORM 更新时，带时间字段的模型使用 `onupdate=func.now()`。
* 供应商产地地址表和财务信息表已完成 ORM 映射，但尚未实现对应子表 CRUD API。
* `master.supplier_finance_infos` 当前有外键，但 `schema.sql` 尚未定义辅助索引。
* 后端已有查询 Schema，但当前列表接口尚未实现筛选。
* `dev_test_logs` 由开发测试接口动态创建，不属于 `schema.sql` 的正式表结构。

---

## 12. Recommended Next Steps / 后续建议

1. Add database migration management, such as Alembic.
2. Add database-level `updated_at` trigger if non-ORM updates are expected.
3. Add seed data for common material categories, material types, units, supplier types, and currencies.
4. Implement query filters for material and supplier list endpoints.
5. Add constraints or reference tables for code fields such as `base_uom_code`, `supplier_type_code`, and `currency_code`.
6. Add CRUD APIs and schemas for supplier origin addresses and supplier finance info.
7. Consider a unique partial index for the default finance record if each supplier should have only one default finance info row.
8. Add indexes on `master.supplier_finance_infos(supplier_id)` and `master.supplier_finance_infos(is_active)` if these filters are common.

1. 增加数据库迁移工具，例如 Alembic。
2. 如果存在非 ORM 更新，建议增加数据库级 `updated_at` 触发器。
3. 增加物料分类、物料类型、单位、供应商类型、币种等基础字典种子数据。
4. 为物料和供应商列表接口实现查询筛选。
5. 为 `base_uom_code`、`supplier_type_code`、`currency_code` 等编码字段增加约束或字典表。
6. 为供应商产地地址和供应商财务信息增加 CRUD API 与 Schema。
7. 如果每个供应商只允许一条默认财务信息，建议增加默认财务信息的 partial unique index。
8. 如果经常按供应商或启用状态筛选财务信息，建议增加 `master.supplier_finance_infos(supplier_id)` 和 `master.supplier_finance_infos(is_active)` 索引。

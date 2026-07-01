CREATE SCHEMA IF NOT EXISTS master;

CREATE SEQUENCE IF NOT EXISTS master.prod_seq START 1;
CREATE SEQUENCE IF NOT EXISTS master.cons_seq START 1;
CREATE SEQUENCE IF NOT EXISTS master.stor_seq START 1;

CREATE TABLE IF NOT EXISTS master.materials (
    id BIGSERIAL PRIMARY KEY,

    material_code VARCHAR(50) NOT NULL UNIQUE,
    material_name_cn VARCHAR(200) NOT NULL,
    material_name_en VARCHAR(200),

    material_category_code VARCHAR(50) NOT NULL,
    material_type_code VARCHAR(50) NOT NULL,
    base_uom_code VARCHAR(20) NOT NULL,

    specification VARCHAR(200),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    remark TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_materials_name_cn
ON master.materials (material_name_cn);

CREATE INDEX IF NOT EXISTS idx_materials_category_code
ON master.materials (material_category_code);

CREATE INDEX IF NOT EXISTS idx_materials_type_code
ON master.materials (material_type_code);

CREATE INDEX IF NOT EXISTS idx_materials_is_active
ON master.materials (is_active);

-- =====================================================
-- Supplier
-- Schema: master
-- Table: suppliers
-- Purpose:
-- Stores supplier identity and primary contact information.
-- Tax, invoice, bank, payment, and origin address details
-- are stored in supplier child tables.
-- =====================================================

CREATE TABLE IF NOT EXISTS master.suppliers (
    id BIGSERIAL PRIMARY KEY,
    -- Basic supplier information
    supplier_id VARCHAR(50) NOT NULL UNIQUE,
    supplier_name_cn VARCHAR(200) NOT NULL,
    supplier_name_en VARCHAR(200) NULL,
    supplier_short_code VARCHAR(50) NULL,
    supplier_type_code VARCHAR(50) NULL,
    -- Contact information
    contact_name VARCHAR(100) NULL,
    phone VARCHAR(50) NULL,
    email VARCHAR(100) NULL,
    -- Status and remarks
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    remark TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_suppliers_name_cn
ON master.suppliers (supplier_name_cn);

CREATE INDEX IF NOT EXISTS idx_suppliers_short_code
ON master.suppliers (supplier_short_code);

CREATE INDEX IF NOT EXISTS idx_suppliers_type_code
ON master.suppliers (supplier_type_code);

CREATE INDEX IF NOT EXISTS idx_suppliers_is_active
ON master.suppliers (is_active);

CREATE SEQUENCE IF NOT EXISTS master.supplier_seq START 1;

-- Suppliers Origin Address Table
CREATE TABLE IF NOT EXISTS master.supplier_origin_addresses (
    id BIGSERIAL PRIMARY KEY,

    supplier_id BIGINT NOT NULL REFERENCES master.suppliers(id) ON DELETE CASCADE,
    origin_address TEXT NOT NULL,

    country VARCHAR(100) NULL,
    province VARCHAR(100) NULL,
    city VARCHAR(100) NULL,
    district VARCHAR(100) NULL,
    postal_code VARCHAR(50) NULL,
    detailed_address VARCHAR(200) NULL,

    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    remark TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_supplier_origin_addresses_supplier_id
ON master.supplier_origin_addresses (supplier_id);

CREATE INDEX IF NOT EXISTS idx_supplier_origin_addresses_is_active
ON master.supplier_origin_addresses (is_active);

CREATE UNIQUE INDEX IF NOT EXISTS uq_supplier_origin_default
ON master.supplier_origin_addresses (supplier_id)
WHERE is_default = TRUE;

-- Supplier Financial Info Table
CREATE TABLE IF NOT EXISTS master.supplier_finance_infos (
    id BIGSERIAL PRIMARY KEY,
    supplier_id BIGINT NOT NULL REFERENCES master.suppliers(id) ON DELETE CASCADE,
    -- Invoice / tax information
    invoice_company_name VARCHAR(200) NULL,
    tax_registration_no VARCHAR(100) NULL,
    invoice_address TEXT NULL,
    invoice_phone VARCHAR(50) NULL,
    -- Bank / payment information
    bank_name VARCHAR(200) NULL,
    bank_account_name VARCHAR(200) NULL,
    bank_account_no VARCHAR(100) NULL,
    currency_code VARCHAR(20) NOT NULL DEFAULT 'CNY',
    -- Status
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    remark TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

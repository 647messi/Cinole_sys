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
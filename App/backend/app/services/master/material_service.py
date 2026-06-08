from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.master.material import Material
from app.repositories.master.material_repository import *
from app.schemas.master.material.create import MaterialCreate
from app.schemas.master.material.update import MaterialUpdate

#------------------- Helper functions ------------------#

MATERIAL_CATEGORY_PREFIX_MAP = {
    "PRODUCTION": "PROD",
    "CONSUMABLE": "CONS",
    "STORAGE": "STOR",
}

def generate_material_code(db: Session, material_category_code: str) -> str:
    category = material_category_code.upper()
    prefix = MATERIAL_CATEGORY_PREFIX_MAP.get(category)
    if not prefix:
        raise HTTPException(status_code=400, detail=f"Unsupported category: {category}")

    # 调用 repository 获取下一个 sequence 值
    next_number = get_next_material_sequence(db, category)

    return f"{prefix}-{next_number:03d}"

#------------------- Service functions ------------------#


def list_materials_service(db: Session) -> list[Material]:
    return get_all_materials(db)


def get_material_service(db: Session, material_id: int) -> Material:
    material = get_material_by_id(db, material_id)

    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")

    return material


def create_material_service(db: Session, payload: MaterialCreate) -> Material:
    material_code = generate_material_code(db, payload.material_category_code)

    material = Material(
        material_code=material_code,
        material_name_cn=payload.material_name_cn,
        material_name_en=payload.material_name_en,
        material_category_code=payload.material_category_code,
        material_type_code=payload.material_type_code,
        base_uom_code=payload.base_uom_code,
        specification=payload.specification,
        remark=payload.remark,
        is_active=True,
    )

    return create_material(db, material)


def update_material_service(
    db: Session,
    material_id: int,
    payload: MaterialUpdate,
) -> Material:
    material = get_material_by_id(db, material_id)

    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(material, field, value)

    return update_material(db, material)

def update_material_status_service(
    db: Session,
    material_id: int,
    is_active: bool,
) -> Material:
    material = get_material_by_id(db, material_id)

    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")

    material.is_active = is_active

    return update_material(db, material)
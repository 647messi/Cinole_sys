from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.master.raw_material_dict_model import Material
from app.repositories.master.raw_material_dict_repository import *
from app.schemas.master.raw_material_dict.create import MaterialCreate
from app.schemas.master.raw_material_dict.update import MaterialUpdate

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
    material = Material(
        **payload.model_dump(),
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

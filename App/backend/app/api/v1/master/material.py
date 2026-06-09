from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.master.material import MaterialCreate, MaterialUpdate, MaterialResponse
from app.services.master.material_service import *

router = APIRouter(
    prefix="/master/materials",
    tags=["Master - Materials"],
)


@router.get("", response_model=list[MaterialResponse])
def list_materials(db: Session = Depends(get_db)):
    return list_materials_service(db)


@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(
    material_id: int,
    db: Session = Depends(get_db),
):
    return get_material_service(db, material_id)


@router.post("", response_model=MaterialResponse)
def create_material(
    payload: MaterialCreate,
    db: Session = Depends(get_db),
):
    return create_material_service(db, payload)


@router.put("/{material_id}", response_model=MaterialResponse)
def update_material(
    material_id: int,
    payload: MaterialUpdate,
    db: Session = Depends(get_db),
):
    return update_material_service(db, material_id, payload)


@router.patch("/{material_id}/status", response_model=MaterialResponse)
def update_material_status(
    material_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
):
    return update_material_status_service(db, material_id, is_active)
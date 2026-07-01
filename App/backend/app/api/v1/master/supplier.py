from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.master.supplier import (
    SupplierCreate,
    SupplierOriginAddressResponse,
    SupplierResponse,
    SupplierUpdate,
)
from app.services.master.supplier_service import *

router = APIRouter(
    prefix="/master/suppliers",
    tags=["Master - Suppliers"]
)

# Get all suppliers
@router.get("", response_model=list[SupplierResponse])
def list_suppliers(db: Session = Depends(get_db)):
    return list_suppliers_service(db)

# Get Supplier by variables
@router.get("/list", response_model=list[SupplierResponse])
def list_suppliers_by_variables(db: Session = Depends(get_db)):
    return list_suppliers_by_variables_service(db)

# Get Supplier by required columns
@router.get("/bycolumns", response_model=list[dict[str, Any]])
def list_suppliers_by_required_columns(
    col_names: list[str] = Query(...),
    db: Session = Depends(get_db),
):
    return list_suppliers_by_required_columns_service(db, col_names)

# Get Supplier Origin Addresses by Supplier ID
@router.get("/{supplier_id}/origin-addresses", response_model=list[SupplierOriginAddressResponse])
def list_supplier_origin_addresses(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    return list_supplier_origin_addresses_service(db, supplier_id)

@router.get("/{supplier_pk}", response_model=SupplierResponse)
def get_supplier(supplier_pk: int, db: Session = Depends(get_db)):
    return get_supplier_service(db, supplier_pk)

@router.post("", response_model=SupplierResponse)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    return create_supplier_service(db, payload)

@router.put("/{supplier_pk}", response_model=SupplierResponse)
def update_supplier(supplier_pk: int, payload: SupplierUpdate, db: Session = Depends(get_db)):
    return update_supplier_service(db, supplier_pk, payload)

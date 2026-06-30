from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.master.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from app.services.master.supplier_service import *

router = APIRouter(
    prefix="/master/suppliers",
    tags=["Master - Suppliers"]
)

# Get all suppliers
@router.get("", response_model=list[SupplierResponse])
def list_suppliers(db: Session = Depends(get_db)):
    return list_suppliers_service(db)

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return get_supplier_service(db, supplier_id)

# Get Supplier by variables
@router.get("/list", response_model=list[SupplierResponse])
def list_suppliers_by_variables(db: Session = Depends(get_db)):
    return list_suppliers_by_variables_service(db)

@router.post("", response_model=SupplierResponse)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    return create_supplier_service(db, payload)

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: int, payload: SupplierUpdate, db: Session = Depends(get_db)):
    return update_supplier_service(db, supplier_id, payload)
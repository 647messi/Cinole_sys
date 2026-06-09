from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.master.supplier_model import Supplier
from app.repositories.master.supplier_repository import *
from app.schemas.master.supplier import SupplierCreate, SupplierUpdate

# ------------------- Helper Functions -------------------
def get_next_supplier_sequence(db: Session) -> int:
    result = db.execute(
        text("SELECT nextval('master.supplier_seq')")
    )
    return result.scalar_one()

def generate_supplier_code(db: Session) -> str:
    """
    Generate a new supplier code using the sequence.
    Format: SUP-001, SUP-002, etc.
    """
    next_number = get_next_supplier_sequence(db)
    return f"SUP-{next_number:04d}"

# ------------------- Service Functions -------------------

def create_supplier_service(db: Session, payload: SupplierCreate) -> Supplier:
    supplier_code = generate_supplier_code(db)

    supplier = Supplier(
        supplier_code=supplier_code,
        **payload.model_dump(),
    )

    return create_supplier(db, supplier)


def update_supplier_service(db: Session, supplier_id: int, payload: SupplierUpdate) -> Supplier:
    """
    Update an existing supplier record.
    """
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)

    return update_supplier(db, supplier)


def get_supplier_service(db: Session, supplier_id: int) -> Supplier:
    """
    Get a single supplier by ID.
    """
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


def list_suppliers_service(db: Session) -> list[Supplier]:
    """
    List all suppliers.
    """
    return list_suppliers(db)
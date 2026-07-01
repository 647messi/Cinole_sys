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

def generate_supplier_id(db: Session) -> str:
    """
    Generate a new supplier business ID using the sequence.
    Format: SUP-001, SUP-002, etc.
    """
    next_number = get_next_supplier_sequence(db)
    return f"SUP-{next_number:04d}"

# ------------------- Service Functions -------------------

def create_supplier_service(db: Session, payload: SupplierCreate) -> Supplier:
    supplier_id = generate_supplier_id(db)

    supplier = Supplier(
        supplier_id=supplier_id,
        **payload.model_dump(),
    )

    return create_supplier(db, supplier)


def update_supplier_service(db: Session, supplier_pk: int, payload: SupplierUpdate) -> Supplier:
    """
    Update an existing supplier record.
    """
    supplier = get_supplier(db, supplier_pk)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)

    return update_supplier(db, supplier)


def get_supplier_service(db: Session, supplier_pk: int) -> Supplier:
    """
    Get a single supplier by ID.
    """
    supplier = get_supplier(db, supplier_pk)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


def list_suppliers_service(db: Session, amount: int = None) -> list[Supplier]:
    """
    List all suppliers.
    """
    return list_suppliers(db, amount=amount)

def list_suppliers_by_required_columns_service(db: Session, col_names: list[str]) -> list[dict]:
    """
    List all columns in the supplier table.
    """
    return list_suppliers_by_required_columns(db, col_names)

def list_suppliers_by_variables_service(db: Session, **kwargs) -> list[Supplier]:
    """
    List suppliers based on certain variables.
    This is a placeholder for actual filtering logic.
    """
    return list_suppliers_by_variables(db, **kwargs)

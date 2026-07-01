from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.master.supplier_model import Supplier

def get_supplier(db: Session, supplier_pk: int):
    return db.query(Supplier).filter(Supplier.id == supplier_pk).first()

# List all columns in supplier table
def list_suppliers(db: Session, amount: int = None):
    if amount is None:
        return db.query(Supplier).all()
    else:
        return db.query(Supplier).limit(amount).all()

# List suppliers in required columns
def list_suppliers_by_required_columns(db: Session, col_names: list[str]):
    invalid_columns = [col for col in col_names if not hasattr(Supplier, col)]
    if invalid_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid supplier columns: {', '.join(invalid_columns)}",
        )

    columns = [getattr(Supplier, col) for col in col_names]
    rows = db.query(*columns).all()
    return [dict(row._mapping) for row in rows]

# List suppliers in required variables
def list_suppliers_by_variables(db: Session, **kwargs):
    query = db.query(Supplier)
    for key, value in kwargs.items():
        if hasattr(Supplier, key):
            query = query.filter(getattr(Supplier, key) == value)
    return query.all()

def create_supplier(db: Session, supplier: Supplier):
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def update_supplier(db: Session, supplier: Supplier):
    db.commit()
    db.refresh(supplier)
    return supplier

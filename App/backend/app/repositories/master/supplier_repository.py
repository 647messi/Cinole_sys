from sqlalchemy.orm import Session
from app.models.master.supplier_model import Supplier

def get_supplier(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def list_suppliers(db: Session):
    return db.query(Supplier).all()

def create_supplier(db: Session, supplier: Supplier):
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def update_supplier(db: Session, supplier: Supplier):
    db.commit()
    db.refresh(supplier)
    return supplier
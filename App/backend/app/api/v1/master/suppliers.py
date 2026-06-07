# app/api/v1/master/suppliers.py

from fastapi import APIRouter

router = APIRouter(
    prefix="/master/suppliers",
    tags=["Master - Suppliers"],
)


@router.get("")
def list_suppliers():
    return {"message": "supplier list"}


@router.get("/{supplier_id}")
def get_supplier(supplier_id: int):
    return {"supplier_id": supplier_id}


@router.post("")
def create_supplier():
    return {"message": "supplier created"}


@router.put("/{supplier_id}")
def update_supplier(supplier_id: int):
    return {"message": f"supplier {supplier_id} updated"}


@router.patch("/{supplier_id}/status")
def update_supplier_status(supplier_id: int):
    return {"message": f"supplier {supplier_id} status updated"}
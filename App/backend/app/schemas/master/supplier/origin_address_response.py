from datetime import datetime

from pydantic import BaseModel


class SupplierOriginAddressResponse(BaseModel):
    id: int
    supplier_id: int
    origin_address: str

    country: str | None = None
    province: str | None = None
    city: str | None = None
    district: str | None = None
    postal_code: str | None = None
    detailed_address: str | None = None

    is_default: bool
    is_active: bool
    remark: str | None = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

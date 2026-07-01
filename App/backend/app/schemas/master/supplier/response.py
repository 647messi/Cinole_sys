from datetime import datetime
from pydantic import BaseModel


class SupplierResponse(BaseModel):
    id: int
    supplier_id: str

    supplier_name_cn: str
    supplier_name_en: str | None = None
    supplier_short_code: str | None = None
    supplier_type_code: str | None = None

    contact_name: str | None = None
    phone: str | None = None
    email: str | None = None

    is_active: bool
    remark: str | None = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

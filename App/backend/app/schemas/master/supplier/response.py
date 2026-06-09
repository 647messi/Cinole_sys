from datetime import datetime
from pydantic import BaseModel


class SupplierResponse(BaseModel):
    id: int
    supplier_code: str

    supplier_name_cn: str
    supplier_name_en: str | None = None
    supplier_short_code: str | None = None
    supplier_type_code: str | None = None

    contact_name: str | None = None
    position_title: str | None = None
    phone: str | None = None
    email: str | None = None

    tax_registration_no: str | None = None
    invoice_company_name: str | None = None
    invoice_address: str | None = None
    invoice_phone: str | None = None

    bank_name: str | None = None
    bank_account_name: str | None = None
    bank_account_no: str | None = None
    currency_code: str

    entrusted_person_name: str | None = None
    legal_representative: str | None = None

    is_active: bool
    remark: str | None = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
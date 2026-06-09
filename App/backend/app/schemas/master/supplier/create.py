from pydantic import BaseModel, Field

class SupplierCreate(BaseModel):
    supplier_name_cn: str = Field(..., min_length=1, max_length=200)
    supplier_name_en: str | None = Field(default=None, max_length=200)
    supplier_short_code: str | None = Field(default=None, max_length=50)
    supplier_type_code: str | None = Field(default=None, max_length=50)

    contact_name: str | None = Field(default=None, max_length=100)
    position_title: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=100)

    tax_registration_no: str | None = Field(default=None, max_length=100)
    invoice_company_name: str | None = Field(default=None, max_length=200)
    invoice_address: str | None = None
    invoice_phone: str | None = Field(default=None, max_length=50)

    bank_name: str | None = Field(default=None, max_length=200)
    bank_account_name: str | None = Field(default=None, max_length=200)
    bank_account_no: str | None = Field(default=None, max_length=100)
    currency_code: str = Field(default="CNY", max_length=20)

    entrusted_person_name: str | None = Field(default=None, max_length=100)
    legal_representative: str | None = Field(default=None, max_length=100)

    remark: str | None = None
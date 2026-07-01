from pydantic import BaseModel, Field


class SupplierUpdate(BaseModel):
    supplier_name_cn: str | None = Field(default=None, min_length=1, max_length=200)
    supplier_name_en: str | None = Field(default=None, max_length=200)
    supplier_short_code: str | None = Field(default=None, max_length=50)
    supplier_type_code: str | None = Field(default=None, max_length=50)

    contact_name: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=100)

    is_active: bool | None = None
    remark: str | None = None

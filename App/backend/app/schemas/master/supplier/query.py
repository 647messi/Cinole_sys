from pydantic import BaseModel, Field

class SupplierQuery(BaseModel):
    keyword: str | None = Field(default=None, max_length=200)
    supplier_type_code: str | None = Field(default=None, max_length=50)
    is_active: bool | None = None
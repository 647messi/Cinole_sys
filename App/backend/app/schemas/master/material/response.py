from datetime import datetime
from pydantic import BaseModel

class MaterialResponse(BaseModel):
    id: int
    material_code: str

    material_name_cn: str
    material_name_en: str | None = None

    material_category_code: str
    material_type_code: str
    base_uom_code: str

    specification: str | None = None
    is_active: bool
    remark: str | None = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
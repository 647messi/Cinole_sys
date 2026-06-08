from pydantic import BaseModel

class MaterialQuery(BaseModel):
    material_category_code: str | None = None
    material_type_code: str | None = None
    is_active: bool | None = None
from pydantic import BaseModel

class MaterialResponse(BaseModel):
    id: int
    material_code: str

    material_name_cn: str
    material_name_en: str | None = None

    base_uom_code: str

    is_active: bool
    remark: str | None = None

    class Config:
        from_attributes = True

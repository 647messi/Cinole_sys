from pydantic import BaseModel, Field


class MaterialCreate(BaseModel):
    material_code: str = Field(..., min_length=1, max_length=50)
    material_name_cn: str = Field(..., min_length=1, max_length=200)
    material_name_en: str | None = Field(default=None, max_length=200)

    base_uom_code: str = Field(..., min_length=1, max_length=20)

    remark: str | None = None

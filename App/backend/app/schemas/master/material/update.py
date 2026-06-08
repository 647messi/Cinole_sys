from pydantic import BaseModel, Field


class MaterialUpdate(BaseModel):
    material_name_cn: str | None = Field(default=None, min_length=1, max_length=200)
    material_name_en: str | None = Field(default=None, max_length=200)

    material_category_code: str | None = Field(default=None, min_length=1, max_length=50)
    material_type_code: str | None = Field(default=None, min_length=1, max_length=50)
    base_uom_code: str | None = Field(default=None, min_length=1, max_length=20)

    specification: str | None = Field(default=None, max_length=200)
    remark: str | None = None
    is_active: bool | None = None
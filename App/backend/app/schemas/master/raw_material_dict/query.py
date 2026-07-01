from pydantic import BaseModel

class MaterialQuery(BaseModel):
    is_active: bool | None = None

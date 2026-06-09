from sqlalchemy import BigInteger, Boolean, Column, DateTime, String, Text
from sqlalchemy.sql import func

from app.db.base import Base


class Material(Base):
    __tablename__ = "materials"
    __table_args__ = {"schema": "master"}

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)

    material_code = Column(String(50), nullable=False, unique=True, index=True)
    material_name_cn = Column(String(200), nullable=False, index=True)
    material_name_en = Column(String(200), nullable=True)

    material_category_code = Column(String(50), nullable=False, index=True)
    material_type_code = Column(String(50), nullable=False, index=True)
    base_uom_code = Column(String(20), nullable=False)

    specification = Column(String(200), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    remark = Column(Text, nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
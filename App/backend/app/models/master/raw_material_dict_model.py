from sqlalchemy import BigInteger, Boolean, Column, String, Text

from app.db.base import Base


class Material(Base):
    __tablename__ = "materials"
    __table_args__ = {"schema": "master"}

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)

    material_code = Column(String(50), nullable=False, unique=True, index=True)
    material_name_cn = Column(String(200), nullable=False, index=True)
    material_name_en = Column(String(200), nullable=True)

    base_uom_code = Column(String(20), nullable=False)

    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    remark = Column(Text, nullable=True)

from sqlalchemy import BigInteger, Boolean, Column, DateTime, String, Text
from sqlalchemy.sql import func

from app.db.base import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = {"schema": "master"}

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)

    # Basic supplier information
    supplier_code = Column(String(50), nullable=False, unique=True, index=True)
    supplier_name_cn = Column(String(200), nullable=False, index=True)
    supplier_name_en = Column(String(200), nullable=True)
    supplier_short_code = Column(String(50), nullable=True, index=True)
    supplier_type_code = Column(String(50), nullable=True, index=True)

    # Contact information
    contact_name = Column(String(100), nullable=True)
    position_title = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)

    # Tax and invoice information
    tax_registration_no = Column(String(100), nullable=True)
    invoice_company_name = Column(String(200), nullable=True)
    invoice_address = Column(Text, nullable=True)
    invoice_phone = Column(String(50), nullable=True)

    # Bank and payment information
    bank_name = Column(String(200), nullable=True)
    bank_account_name = Column(String(200), nullable=True)
    bank_account_no = Column(String(100), nullable=True)
    currency_code = Column(String(20), nullable=False, default="CNY", server_default="CNY")

    # Legal / authorization information
    entrusted_person_name = Column(String(100), nullable=True)
    legal_representative = Column(String(100), nullable=True)

    # Status and remarks
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    remark = Column(Text, nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
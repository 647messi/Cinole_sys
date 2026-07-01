from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = {"schema": "master"}

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)

    # Basic supplier information
    supplier_id = Column(String(50), nullable=False, unique=True, index=True)
    supplier_name_cn = Column(String(200), nullable=False, index=True)
    supplier_name_en = Column(String(200), nullable=True)
    supplier_short_code = Column(String(50), nullable=True, index=True)
    supplier_type_code = Column(String(50), nullable=True, index=True)

    # Contact information
    contact_name = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)

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

    origin_addresses = relationship(
        "SupplierOriginAddress",
        back_populates="supplier",
        cascade="all, delete-orphan",
    )
    finance_infos = relationship(
        "SupplierFinanceInfo",
        back_populates="supplier",
        cascade="all, delete-orphan",
    )


class SupplierOriginAddress(Base):
    __tablename__ = "supplier_origin_addresses"
    __table_args__ = {"schema": "master"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    supplier_id = Column(
        BigInteger,
        ForeignKey("master.suppliers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    origin_address = Column(Text, nullable=False)
    country = Column(String(100), nullable=True)
    province = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    postal_code = Column(String(50), nullable=True)
    detailed_address = Column(String(200), nullable=True)

    is_default = Column(Boolean, nullable=False, default=False, server_default="false")
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")

    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    supplier = relationship("Supplier", back_populates="origin_addresses")


class SupplierFinanceInfo(Base):
    __tablename__ = "supplier_finance_infos"
    __table_args__ = {"schema": "master"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    supplier_id = Column(
        BigInteger,
        ForeignKey("master.suppliers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Invoice / tax information
    invoice_company_name = Column(String(200), nullable=True)
    tax_registration_no = Column(String(100), nullable=True)
    invoice_address = Column(Text, nullable=True)
    invoice_phone = Column(String(50), nullable=True)

    # Bank / payment information
    bank_name = Column(String(200), nullable=True)
    bank_account_name = Column(String(200), nullable=True)
    bank_account_no = Column(String(100), nullable=True)
    currency_code = Column(String(20), nullable=False, default="CNY", server_default="CNY")

    # Status
    is_default = Column(Boolean, nullable=False, default=False, server_default="false")
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    supplier = relationship("Supplier", back_populates="finance_infos")

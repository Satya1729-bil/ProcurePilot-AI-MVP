from datetime import datetime, timezone
from sqlalchemy import String, Date, DateTime, ForeignKey, Numeric, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

def utcnow(): return datetime.now(timezone.utc)
class Supplier(Base):
    __tablename__='suppliers'
    id: Mapped[str]=mapped_column(String(24),primary_key=True)
    name: Mapped[str]=mapped_column(String(160),nullable=False,index=True)
    category: Mapped[str]=mapped_column(String(100),nullable=False)
    status: Mapped[str]=mapped_column(String(30),default='Active')
    description: Mapped[str]=mapped_column(Text,default='')
class PurchaseOrder(Base):
    __tablename__='purchase_orders'
    id: Mapped[str]=mapped_column(String(24),primary_key=True)
    supplier_id: Mapped[str]=mapped_column(ForeignKey('suppliers.id'),index=True)
    currency: Mapped[str]=mapped_column(String(3),nullable=False)
    total_amount: Mapped[float]=mapped_column(Numeric(12,2),nullable=False)
    status: Mapped[str]=mapped_column(String(30),default='Open')
    description: Mapped[str]=mapped_column(Text,default='')
class Invoice(Base):
    __tablename__='invoices'
    id: Mapped[str]=mapped_column(String(24),primary_key=True)
    supplier_id: Mapped[str]=mapped_column(String(24),nullable=False,index=True)
    purchase_order_id: Mapped[str|None]=mapped_column(String(24),nullable=True,index=True)
    currency: Mapped[str]=mapped_column(String(3),nullable=False)
    total_amount: Mapped[float]=mapped_column(Numeric(12,2),nullable=False)
    invoice_date: Mapped[object]=mapped_column(Date,nullable=False)
    status: Mapped[str]=mapped_column(String(30),default='Submitted')
    description: Mapped[str]=mapped_column(Text,default='')
class Contract(Base):
    __tablename__='contracts'
    id: Mapped[str]=mapped_column(String(24),primary_key=True)
    supplier_id: Mapped[str]=mapped_column(ForeignKey('suppliers.id'),index=True)
    title: Mapped[str]=mapped_column(String(180),nullable=False)
    expiry_date: Mapped[object]=mapped_column(Date,nullable=False)
    terms_summary: Mapped[str]=mapped_column(Text,default='')
class ExceptionRecord(Base):
    __tablename__='exceptions'
    id: Mapped[str]=mapped_column(String(24),primary_key=True)
    invoice_id: Mapped[str]=mapped_column(ForeignKey('invoices.id'),index=True)
    severity: Mapped[str]=mapped_column(String(20),default='Medium')
    reason: Mapped[str]=mapped_column(Text,nullable=False)
    review_status: Mapped[str]=mapped_column(String(30),default='Open')
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow,onupdate=utcnow)
class AuditEvent(Base):
    __tablename__='audit_events'
    id: Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    entity_type: Mapped[str]=mapped_column(String(40),nullable=False)
    entity_id: Mapped[str]=mapped_column(String(24),nullable=False)
    action: Mapped[str]=mapped_column(String(80),nullable=False)
    actor_id: Mapped[str]=mapped_column(String(80),default='demo-user')
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
    details: Mapped[dict]=mapped_column(JSON,default=dict)

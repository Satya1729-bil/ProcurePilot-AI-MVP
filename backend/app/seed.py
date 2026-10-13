from datetime import date
from sqlalchemy.orm import Session
from .models import Supplier, PurchaseOrder, Invoice, Contract

def seed_demo_data(db: Session):
    suppliers=[
      Supplier(id='SUP-100',name='Northstar Office Supplies',category='Office supplies',status='Active',description='Synthetic office supply vendor.'),
      Supplier(id='SUP-200',name='BluePeak IT Services',category='IT services',status='Active',description='Synthetic managed IT and cloud services vendor.'),
      Supplier(id='SUP-300',name='Greenline Logistics',category='Logistics',status='Review',description='Synthetic freight and warehouse services vendor.')]
    for x in suppliers:
      if not db.get(Supplier,x.id): db.add(x)
    db.flush()
    pos=[PurchaseOrder(id='PO-500',supplier_id='SUP-100',currency='USD',total_amount=1200,status='Open',description='Office supply replenishment.'),PurchaseOrder(id='PO-600',supplier_id='SUP-200',currency='USD',total_amount=4800,status='Open',description='Quarterly IT support.'),PurchaseOrder(id='PO-700',supplier_id='SUP-300',currency='USD',total_amount=2250,status='Open',description='Domestic logistics services.')]
    for x in pos:
      if not db.get(PurchaseOrder,x.id): db.add(x)
    invoices=[Invoice(id='INV-900',supplier_id='SUP-100',purchase_order_id='PO-500',currency='USD',total_amount=1200,invoice_date=date(2026,9,4),status='Submitted',description='Office supplies invoice.'),Invoice(id='INV-901',supplier_id='SUP-200',purchase_order_id='PO-600',currency='USD',total_amount=5100,invoice_date=date(2026,9,9),status='Submitted',description='IT support invoice; total may differ from PO.'),Invoice(id='INV-902',supplier_id='SUP-300',purchase_order_id='PO-700',currency='EUR',total_amount=2250,invoice_date=date(2026,9,11),status='Submitted',description='Logistics invoice; currency requires review.'),Invoice(id='INV-903',supplier_id='SUP-100',purchase_order_id='PO-MISSING',currency='USD',total_amount=100,invoice_date=date(2026,9,13),status='Submitted',description='Invoice with unresolved PO reference.')]
    for x in invoices:
      if not db.get(Invoice,x.id): db.add(x)
    contracts=[Contract(id='CON-100',supplier_id='SUP-100',title='Office Supplies Agreement',expiry_date=date(2026,11,15),terms_summary='Synthetic agreement; renewal requires human review.'),Contract(id='CON-200',supplier_id='SUP-200',title='IT Support Services Agreement',expiry_date=date(2027,3,31),terms_summary='Synthetic quarterly IT support agreement.'),Contract(id='CON-300',supplier_id='SUP-300',title='Logistics Services Agreement',expiry_date=date(2026,10,30),terms_summary='Synthetic logistics agreement; verify expiry with source contract.')]
    for x in contracts:
      if not db.get(Contract,x.id): db.add(x)
    db.commit()

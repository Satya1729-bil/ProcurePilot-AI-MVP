from types import SimpleNamespace
from decimal import Decimal
from app.services import validate_invoice, retrieve, answer_question
class Query:
    def __init__(self,result=None): self.result=result
    def filter(self,*a,**k): return self
    def first(self): return self.result
class DB:
    def __init__(self,po=None,existing=None): self.po=po; self.existing=existing; self.added=[]
    def get(self,model,key): return self.po if model.__name__=='PurchaseOrder' and self.po and self.po.id==key else None
    def query(self,model): return Query(self.existing)
    def add(self,obj): self.added.append(obj)
    def commit(self): pass
def invoice(**kw):
    d=dict(id='INV-1',supplier_id='SUP-1',purchase_order_id='PO-1',currency='USD',total_amount=Decimal('100.00')); d.update(kw); return SimpleNamespace(**d)
def po(**kw):
    d=dict(id='PO-1',supplier_id='SUP-1',currency='USD',total_amount=Decimal('100.00')); d.update(kw); return SimpleNamespace(**d)
def test_matching_invoice_passes():
    r=validate_invoice(DB(po=po()),invoice()); assert r['status']=='No discrepancy found' and not r['discrepancies']
def test_total_mismatch_flags_exception():
    r=validate_invoice(DB(po=po()),invoice(total_amount=Decimal('130.00'))); assert r['status']=='Needs review' and r['discrepancies'][0]['field']=='total_amount'
def test_supplier_and_currency_mismatches():
    r=validate_invoice(DB(po=po()),invoice(supplier_id='SUP-X',currency='EUR')); assert {x['field'] for x in r['discrepancies']}=={'supplier_id','currency'}
def test_missing_po_flags_review():
    r=validate_invoice(DB(),invoice(purchase_order_id='PO-MISSING')); assert r['status']=='Needs review'
def test_retrieval_finds_invoice():
    rows=[{'source_id':'INV-9','source_type':'invoice','title':'Invoice INV-9','text':'Invoice INV-9 amount 700 USD'},{'source_id':'CON-1','source_type':'contract','title':'Contract','text':'Expires in 2027'}]
    assert retrieve('What is invoice INV-9 amount?',rows)[0]['source_id']=='INV-9'
def test_no_evidence_does_not_guess():
    r=answer_question('Weather on Mars?',[]); assert r['mode']=='no-evidence' and r['sources']==[]

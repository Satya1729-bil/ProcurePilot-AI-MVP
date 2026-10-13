import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from .db import Base, engine, get_db, SessionLocal
from . import models
from .seed import seed_demo_data
from .services import validate_invoice, corpus_records, answer_question

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db: seed_demo_data(db)
    yield
app=FastAPI(title='ProcurePilot AI API',version='1.0.0',description='Portfolio MVP with synthetic data; not for payment decisions.',lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=os.getenv('CORS_ORIGINS','http://localhost:5173').split(','),allow_credentials=False,allow_methods=['*'],allow_headers=['*'])
class StatusUpdate(BaseModel):
    review_status: str=Field(pattern='^(Open|Under review|Resolved|Escalated)$')
    actor_id: str=Field(default='demo-user',max_length=80)
class AskRequest(BaseModel): question: str=Field(min_length=3,max_length=1000)
@app.get('/health')
def health(): return {'status':'ok','app':'ProcurePilot AI','data':'synthetic demo data'}
@app.get('/api/dashboard')
def dashboard(db:Session=Depends(get_db)):
    total=db.query(models.Invoice).count(); count=db.query(models.ExceptionRecord).count()
    opened=db.query(models.ExceptionRecord).filter(models.ExceptionRecord.review_status!='Resolved').count()
    resolved=db.query(models.ExceptionRecord).filter(models.ExceptionRecord.review_status=='Resolved').count()
    return {'total_invoices':total,'exceptions':count,'open_exceptions':opened,'resolved_exceptions':resolved,'synthetic_data':True,'note':'Metrics describe seeded demo records, not production performance.'}
@app.get('/api/suppliers')
def suppliers(q:str=Query(default='',max_length=100),db:Session=Depends(get_db)):
    query=db.query(models.Supplier)
    if q: query=query.filter(models.Supplier.name.ilike(f'%{q}%')|models.Supplier.id.ilike(f'%{q}%'))
    return [{'id':s.id,'name':s.name,'category':s.category,'status':s.status,'description':s.description} for s in query.order_by(models.Supplier.name).all()]
@app.get('/api/invoices')
def invoices(db:Session=Depends(get_db)):
    return [{'id':i.id,'supplier_id':i.supplier_id,'purchase_order_id':i.purchase_order_id,'currency':i.currency,'total_amount':float(i.total_amount),'invoice_date':i.invoice_date.isoformat(),'status':i.status,'description':i.description} for i in db.query(models.Invoice).order_by(models.Invoice.invoice_date.desc()).all()]
@app.get('/api/exceptions')
def exceptions(db:Session=Depends(get_db)):
    return [{'id':e.id,'invoice_id':e.invoice_id,'severity':e.severity,'reason':e.reason,'review_status':e.review_status,'created_at':e.created_at.isoformat() if e.created_at else None} for e in db.query(models.ExceptionRecord).order_by(models.ExceptionRecord.created_at.desc()).all()]
@app.post('/api/invoices/{invoice_id}/validate')
def validate(invoice_id:str,db:Session=Depends(get_db)):
    invoice=db.get(models.Invoice,invoice_id)
    if not invoice: raise HTTPException(status_code=404,detail='Invoice not found')
    return validate_invoice(db,invoice)
@app.patch('/api/exceptions/{exception_id}/status')
def update_status(exception_id:str,payload:StatusUpdate,db:Session=Depends(get_db)):
    item=db.get(models.ExceptionRecord,exception_id)
    if not item: raise HTTPException(status_code=404,detail='Exception not found')
    item.review_status=payload.review_status; item.updated_at=models.utcnow()
    db.add(models.AuditEvent(entity_type='exception',entity_id=item.id,action='review_status_changed',actor_id=payload.actor_id,details={'review_status':payload.review_status}))
    db.commit(); db.refresh(item)
    return {'id':item.id,'review_status':item.review_status,'updated_at':item.updated_at.isoformat(),'note':'Review status is not payment approval.'}
@app.post('/api/ask')
def ask(payload:AskRequest,db:Session=Depends(get_db)):
    return answer_question(payload.question,corpus_records(db),os.getenv('OPENAI_API_KEY',''),os.getenv('OPENAI_MODEL','gpt-4o-mini'))

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from .database import get_db, engine, Base
from .schemas import UserCreate, RecordCreate, RecordOut, Summary
from .crud import create_user, create_record, get_records, get_summary
from .auth import get_current_user, require_admin, require_analyst_or_admin

# Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Dashboard API")

@app.on_event("startup")
def seed():
    db = next(get_db())
    try:
        create_user(db, UserCreate(username="admin1", role="admin"))
        create_user(db, UserCreate(username="analyst1", role="analyst"))
        print("✅ SEED OK")
    except:
        pass
    db.close()

@app.get("/")
def root():
    return {"status": "OK", "docs": "/docs"}

@app.post("/records/", response_model=RecordOut)
def create_record(record: RecordCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return create_record(db, record, 1)

@app.get("/records/")
def read_records(skip: int = Query(0), limit: int = Query(100), category: str = Query(None), 
                 db: Session = Depends(get_db), user=Depends(require_analyst_or_admin)):
    return get_records(db, skip, limit, category)

@app.get("/dashboard/summary", response_model=Summary)
def summary(db: Session = Depends(get_db), user=Depends(require_analyst_or_admin)):
    return get_summary(db)
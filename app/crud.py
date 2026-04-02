from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from typing import Optional

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_records(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None):
    query = db.query(models.Record)
    if category:
        query = query.filter(models.Record.category == category)
    return query.offset(skip).limit(limit).all()

def create_record(db: Session, record: schemas.RecordCreate, user_id: int):
    db_record = models.Record(
        amount=record.amount,
        type=record.type,
        category=record.category,
        date=record.date,
        notes=record.notes,
        user_id=user_id
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_summary(db: Session):
    income = db.query(func.sum(models.Record.amount)).filter(models.Record.type == 'income').scalar() or 0
    expenses = db.query(func.sum(models.Record.amount)).filter(models.Record.type == 'expense').scalar() or 0
    
    cats = db.query(models.Record.category, func.sum(models.Record.amount)).group_by(models.Record.category).all()
    categories = {cat[0]: float(cat[1]) for cat in cats}
    
    return schemas.Summary(
        total_income=float(income),
        total_expenses=float(expenses),
        net_balance=float(income - expenses),
        categories=categories
    )
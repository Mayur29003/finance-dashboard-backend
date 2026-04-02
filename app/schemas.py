from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class Role(str, Enum):
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"

class UserCreate(BaseModel):
    username: str
    role: Role

class UserOut(BaseModel):
    id: int
    username: str
    role: Role
    active: bool = True

    class Config:
        from_attributes = True

class RecordCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be positive")
    type: str  # income or expense
    category: str
    date: datetime
    notes: Optional[str] = None

class RecordOut(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: datetime
    notes: Optional[str] = None
    user_id: int

    class Config:
        from_attributes = True

class Summary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    categories: Dict[str, float]
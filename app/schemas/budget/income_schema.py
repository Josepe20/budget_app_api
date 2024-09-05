from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IncomeBase(BaseModel):
    budget_id: int

class IncomeCreate(IncomeBase):
    amount: Optional[float] = 0
    income_name: Optional[str] = None

class IncomeResponse(IncomeBase):
    budget_id: int
    total_income: float
    total_expense: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True 
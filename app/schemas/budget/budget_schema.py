from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BudgetBase(BaseModel):
    user_id: int

class BudgetCreate(BudgetBase):
    total_income: Optional[float] = 0
    total_expense: Optional[float] = 0

class BudgetResponse(BudgetBase):
    budget_id: int
    total_income: float
    total_expense: float
    created_at: datetime

    class Config:
        orm_mode = True

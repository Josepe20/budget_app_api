from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExpenseBase(BaseModel):
    budget_id: int
    category_expense_id: int

class ExpenseCreate(ExpenseBase):
    amount: Optional[float] = 0
    expense_name: Optional[str] = None

class ExpenseResponse(ExpenseBase):
    expense_id: int
    expense_name: str
    amount: float   
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
        model_config = {"from_attributes": True}

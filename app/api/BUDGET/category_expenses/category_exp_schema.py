from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryExpensesBase(BaseModel):
    category_name: str
    description: str

class CategoryExpensesCreate(CategoryExpensesBase):
    pass

class CategoryExpensesResponse(CategoryExpensesBase):
    category_expense_id: int  
    created_at: datetime 

    class Config:
        orm_mode = True
        from_attributes = True
        model_config = {"from_attributes": True}

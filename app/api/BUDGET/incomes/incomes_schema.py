from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IncomeBase(BaseModel):
    budget_id: int

class IncomeCreate(IncomeBase):
    amount: Optional[float] = 0
    income_name: Optional[str] = None

class IncomeResponse(IncomeBase):
    income_id: int
    income_name: str
    amount: float
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
        model_config = {"from_attributes": True}

        # This will automatically serialize datetime fields to ISO 8601 format
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

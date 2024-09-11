from sqlalchemy import Column, Integer, DateTime, String
from app.database import Base
from datetime import datetime, timezone

class CategoryExpenses(Base):
    __tablename__ = "category_expenses"
    __table_args__ = {"schema": "budget"} 

    category_expense_id = Column(Integer, primary_key=True, index=True)
    description =Column(String(100), default=None)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

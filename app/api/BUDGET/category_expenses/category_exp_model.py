from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class CategoryExpenses(Base):
    __tablename__ = "category_expenses"
    __table_args__ = {"schema": "budget"} 

    category_expense_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    description =Column(String(100), default=None)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # One To Many RelationShip
    expenses = relationship("Expenses", back_populates="category_expense")
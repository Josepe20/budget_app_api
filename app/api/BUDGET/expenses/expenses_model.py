from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Expenses(Base):
    __tablename__ = "expenses"
    __table_args__ = {"schema": "budget"} 

    expense_id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey('budget.budget.budget_id', ondelete="CASCADE"), nullable=False)
    category_expense_id = Column(Integer, ForeignKey('budget.category_expenses.category_expense_id'), nullable=False)
    amount = Column(Float, default=0)
    expense_name = Column(String(100), default=None)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Many to One RelationShip with Budget
    budget = relationship("Budget", back_populates="expenses")

    # Many to One RelationShip with CategoryExpenses
    category_expense = relationship("CategoryExpenses", back_populates="expenses")

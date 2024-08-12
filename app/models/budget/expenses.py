from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Expenses(Base):
    __tablename__ = "expenses"
    __table_args__ = {"schema": "budget"} 

    expense_id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey('budget.budget.budget_id'), nullable=False)
    category_expense_id = Column(Integer, ForeignKey('budget.category_expenses.category_expense_id'), nullable=False)
    amount = Column(Float, default=0)
    expense_name = Column(String(100), default=None)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relaciones opcionales con las tablas Budget y CategoryExpense
    budget = relationship("Budget", back_populates="expenses")
    category_expense = relationship("CategoryExpenses", back_populates="expenses")
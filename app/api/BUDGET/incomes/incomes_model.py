from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Incomes(Base):
    __tablename__ = "incomes"
    __table_args__ = {"schema": "budget"}  

    income_id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey('budget.budget.budget_id'), nullable=False)
    amount = Column(Float, default=0)
    income_name = Column(String(100), default=None)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Many-to-One relationship with Budget
    budget = relationship("Budget", back_populates="incomes")
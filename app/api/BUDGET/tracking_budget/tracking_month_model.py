from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class TrackingMonth(Base):
    __tablename__ = "tracking_month"
    __table_args__ = {"schema": "budget"} 

    tracking_month_id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey('budget.budget.budget_id', ondelete="CASCADE"), nullable=False, unique=True)
    month_ = Column(Integer, nullable=False)
    year_ = Column(Integer, nullable=False)
    total_income = Column(Float, default=0)
    total_expense = Column(Float, default=0)
    total_savings = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relación opcional con la tabla Budget
    budget = relationship("Budget", back_populates="tracking_month")

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Budget(Base):
    __tablename__ = "budget"
    __table_args__ = {"schema": "budget"}  # Especifica el esquema

    budget_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.users.user_id'), nullable=False)
    total_income = Column(Float, default=0)
    total_expense = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relación opcional con la tabla de usuarios
    user = relationship("User", back_populates="budgets")
    
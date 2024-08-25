from sqlalchemy.orm import Session
from app.models.budget.budget import Budget
from app.schemas.budget.budget_schema import BudgetCreate, BudgetResponse
from fastapi import HTTPException, status

def get_all_budgets(db: Session):
    return db.query(Budget).all()

def get_budget_by_id(budget_id: int, db: Session):
    budget = db.query(Budget).filter(Budget.budget_id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget

def create_budget(budget: BudgetCreate, db: Session):
    new_budget = Budget(
        user_id=budget.user_id,
        total_income=budget.total_income,
        total_expense=budget.total_expense,
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget

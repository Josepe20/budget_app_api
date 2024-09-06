from sqlalchemy.orm import Session
from app.models.budget.budget import Budget
from app.schemas.budget.budget_schema import BudgetCreate, BudgetResponse
from app.repositories.budget.budget_repository import BudgetRepository
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.functions.validate_active_month import validate_active_month


def get_all_budgets(db: Session):
    budget_repository = BudgetRepository(db)
    return budget_repository.get_all()


def get_all_budgets_by_user(user_id: int, db: Session):
    budget_repository = BudgetRepository(db)

    if len(budget_repository.get_all_by_user_id(user_id)) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budgets not found")

    return budget_repository.get_all_by_user_id(user_id)


def get_budget_by_id(budget_id: int, db: Session):
    budget_repository = BudgetRepository(db)

    budget = budget_repository.get_budget_by_id(budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    
    return budget


def create_budget(budget: BudgetCreate, db: Session):
    budget_repository = BudgetRepository(db)
    current_month = datetime.now().month
    current_year = datetime.now().year

    existing_budget = budget_repository.get_budget_by_user_and_month(budget.user_id, current_month, current_year)
    if existing_budget:
        return existing_budget, False

    new_budget = Budget(
        user_id=budget.user_id,
        total_income=budget.total_income,
        total_expense=budget.total_expense,
        created_at=datetime.now(timezone.utc)
    )
    
    validate_active_month(new_budget.created_at)

    created_budget = budget_repository.create_budget(new_budget)
    return created_budget, True


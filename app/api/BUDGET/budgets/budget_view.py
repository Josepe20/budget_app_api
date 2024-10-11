from sqlalchemy.orm import Session
from app.api.BUDGET.budgets.budget_model import Budget
from app.api.BUDGET.budgets.budget_schema import BudgetCreate, BudgetResponse
from app.api.BUDGET.budgets.budget_repository import BudgetRepository
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.common.functions.validate_active_month import validate_active_month
from app.common.functions.get_obj_or_404 import get_object_or_404, get_list_or_404


def get_all_budgets(db: Session) -> list[BudgetResponse]:
    budget_repository = BudgetRepository(db)  
    return get_object_or_404(budget_repository.get_all(), "No Budgets Found")


def get_all_budgets_by_user(user_id: int, db: Session) -> list[BudgetResponse]:
    budget_repository = BudgetRepository(db)
    budgets = get_list_or_404(budget_repository.get_all_by_user_id(user_id), "No Budgets Found")
    return budgets


def get_budget_by_id(budget_id: int, db: Session) -> BudgetResponse:
    budget_repository = BudgetRepository(db)
    budget = get_object_or_404(budget_repository.get_budget_by_id(budget_id), "Budget Not Found")
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


def update_budget_totals(budget_id: int, type: str, operation: str, amount: float, db: Session) -> BudgetResponse:
    budget_repository = BudgetRepository(db)

    budget = get_object_or_404(budget_repository.get_budget_by_id(budget_id), "Budget Not Found")

    # Determine whether we are going to add or restart according to the type of operation
    if type == "income":
        if operation == "sum":
            budget.total_income += amount
        elif operation == "sub":
            budget.total_income -= amount
    elif type == "expense":
        if operation == "sum":
            budget.total_expense += amount
        elif operation == "sub":
            budget.total_expense -= amount

    budget_repository.update_budget(budget)
    

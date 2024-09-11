from sqlalchemy.orm import Session
from app.api.BUDGET.incomes.incomes_model import Incomes
from app.api.BUDGET.incomes.incomes_schema import IncomeCreate, IncomeResponse
from app.api.BUDGET.incomes.incomes_repository import IncomeRepository
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.common.functions.validate_active_month import validate_active_month
from app.api.BUDGET.budgets.budget_view import update_budget_totals


def create_income(income_data: IncomeCreate, db: Session):
    income_repository = IncomeRepository(db)
    new_income = Incomes(
        budget_id=income_data.budget_id,
        amount=income_data.amount,
        income_name=income_data.income_name,
        created_at=datetime.now(timezone.utc)
    )

    validate_active_month(new_income.created_at)

    created_income = income_repository.create_income(new_income)

    # update the total budget income
    update_budget_totals(
        budget_id=income_data.budget_id, 
        type="income", 
        operation="sum", 
        amount=new_income.amount, 
        db=db
    )

    # Refresh the object state
    db.refresh(created_income)
    return created_income


def update_income(income_id: int, income_data: dict, db: Session):
    income_repository = IncomeRepository(db)

    income_to_update = income_repository.get_income_by_id(income_id)
    if not income_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    
    validate_active_month(income_to_update.created_at)

    # Calculate the difference between the old and new value
    difference = income_data['amount'] - income_to_update.amount

    updated_income = income_repository.update_income(income_id, income_data)

    # update the total budget income
    update_budget_totals(
        budget_id=updated_income.budget_id,
        type="income",
        operation="sum" if difference > 0 else "sub",
        amount=abs(difference),
        db=db
    )

    # Refresh the object state
    db.refresh(updated_income)
    return updated_income


def delete_income(income_id: int, db: Session):
    income_repository = IncomeRepository(db)

    income_to_delete = income_repository.get_income_by_id(income_id)
    if not income_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    
    validate_active_month(income_to_delete.created_at)

    # update the total budget income
    update_budget_totals(
        budget_id=income_to_delete.budget_id, 
        type="income", 
        operation="sub", 
        amount=income_to_delete.amount, 
        db=db
    )

    deleted_income = income_repository.delete_income(income_id)
    return deleted_income


def get_income_by_id(income_id: int, db: Session):
    income_repository = IncomeRepository(db)
    income = income_repository.get_income_by_id(income_id)
    if not income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    return income


def get_user_incomes(user_id: int, db: Session):
    income_repository = IncomeRepository(db)
    incomes = income_repository.get_user_incomes(user_id)
    if not incomes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No incomes found")
    return incomes


def get_user_active_incomes(user_id: int, db: Session):
    income_repository = IncomeRepository(db)
    current_month = datetime.now().month
    current_year = datetime.now().year
    incomes = income_repository.get_user_active_incomes(user_id, current_month, current_year)
    if not incomes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active incomes found")
    return incomes

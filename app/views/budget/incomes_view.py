from sqlalchemy.orm import Session
from app.models.budget.incomes import Incomes
from app.schemas.budget.income_schema import IncomeCreate, IncomeResponse
from app.repositories.budget.incomes_repository import IncomeRepository
from datetime import datetime, timezone
from fastapi import HTTPException, status


def create_income(income_data: IncomeCreate, db: Session):
    income_repository = IncomeRepository(db)
    new_income = Incomes(
        budget_id=income_data.budget_id,
        amount=income_data.amount,
        income_name=income_data.income_name,
        created_at=datetime.now(timezone.utc)
    )
    created_income = income_repository.create_income(new_income)
    return created_income


def update_income(income_id: int, income_data: dict, db: Session):
    income_repository = IncomeRepository(db)
    updated_income = income_repository.update_income(income_id, income_data)
    if not updated_income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    return updated_income


def delete_income(income_id: int, db: Session):
    income_repository = IncomeRepository(db)
    deleted_income = income_repository.delete_income(income_id)
    if not deleted_income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
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

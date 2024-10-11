from sqlalchemy.orm import Session
from app.api.BUDGET.category_expenses.category_exp_repository import CategoryExpensesRepository
from fastapi import HTTPException, status
from app.api.BUDGET.category_expenses.category_exp_schema import CategoryExpensesResponse


def get_all_categories(db: Session) -> list[CategoryExpensesResponse]:
    category_exp_repository = CategoryExpensesRepository(db)
    return category_exp_repository.get_all()


def get_category_by_id(category_id: int, db: Session) -> CategoryExpensesResponse:
    category_exp_repository = CategoryExpensesRepository(db)

    category = category_exp_repository.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Expense not found")
    
    return category
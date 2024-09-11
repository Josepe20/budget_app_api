from sqlalchemy.orm import Session
from app.api.BUDGET.category_expenses.category_exp_repository import CategoryExpensesRepository
from fastapi import HTTPException, status


def get_all_categories(db: Session):
    category_exp_repository = CategoryExpensesRepository(db)
    return category_exp_repository.get_all()


def get_category_by_id(category_id: int, db: Session):
    category_exp_repository = CategoryExpensesRepository(db)

    category = category_exp_repository.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Expense not found")
    
    return category
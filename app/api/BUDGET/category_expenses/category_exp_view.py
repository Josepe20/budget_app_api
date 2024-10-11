from sqlalchemy.orm import Session
from app.api.BUDGET.category_expenses.category_exp_repository import CategoryExpensesRepository
from app.api.BUDGET.category_expenses.category_exp_schema import CategoryExpensesResponse
from app.common.functions.get_obj_or_404 import get_object_or_404, get_list_or_404


def get_all_categories(db: Session) -> list[CategoryExpensesResponse]:
    category_exp_repository = CategoryExpensesRepository(db)

    return get_list_or_404(category_exp_repository.get_all(), "No Category Expenses Found")


def get_category_by_id(category_id: int, db: Session) -> CategoryExpensesResponse:
    category_exp_repository = CategoryExpensesRepository(db)

    category = get_object_or_404(category_exp_repository.get_category_by_id(category_id),"Category Expense not found")
    return category
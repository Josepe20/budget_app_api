from sqlalchemy.orm import Session
from app.api.BUDGET.category_expenses.category_exp_model import CategoryExpenses
from app.api.BUDGET.category_expenses.category_exp_schema import CategoryExpensesResponse


class CategoryExpensesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[CategoryExpensesResponse]:
        categories = self.db.query(CategoryExpenses).all()
        return [CategoryExpensesResponse.model_validate(category) for category in categories]
    
    def get_category_by_id(self, category_expense_id: int) -> CategoryExpenses:
        return self.db.query(CategoryExpenses).filter(CategoryExpenses.category_expense_id == category_expense_id).first()
    
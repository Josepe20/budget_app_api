from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.api.BUDGET.budgets.budget_model import Budget
from app.api.BUDGET.expenses.expenses_model import Expenses


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_expense(self, expense: Expenses) -> Expenses:
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def update_expense(self, expense_id: int, new_data: dict) -> Expenses:
        expense = self.db.query(Expenses).filter(Expenses.expense_id == expense_id).first()
        if expense:
            for key, value in new_data.items():
                setattr(expense, key, value)
            self.db.commit()
            self.db.refresh(expense)
        return expense

    def delete_expense(self, expense_id: int) -> Expenses:
        expense = self.db.query(Expenses).filter(Expenses.expense_id == expense_id).first()
        if expense:
            self.db.delete(expense)
            self.db.commit()
        return expense

    def get_expense_by_id(self, expense_id: int) -> Expenses:
        return self.db.query(Expenses).filter(Expenses.expense_id == expense_id).first()

    def get_user_expenses(self, user_id: int) -> list[Expenses]:
        return self.db.query(Expenses).join(Budget).filter(Budget.user_id == user_id).all()

    def get_user_active_expenses(self, user_id: int, current_month: int, current_year: int) -> list[Expenses]:
        return self.db.query(Expenses).join(Budget).filter(
            Budget.user_id == user_id,
            extract('month', Budget.created_at) == current_month,
            extract('year', Budget.created_at) == current_year
        ).all()
    
    def get_user_expenses_by_category(self, user_id: int, category_id: int) -> list[Expenses]:
        return self.db.query(Expenses).join(Budget).filter(
            Budget.user_id == user_id,
            Expenses.category_expense_id == category_id
        ).all()

    def get_user_active_expenses_by_category(self, user_id: int, category_id: int, current_month: int, current_year: int) -> list[Expenses]:
        return self.db.query(Expenses).join(Budget).filter(
            Budget.user_id == user_id,
            Expenses.category_expense_id == category_id,
            extract('month', Budget.created_at) == current_month,
            extract('year', Budget.created_at) == current_year
        ).all()
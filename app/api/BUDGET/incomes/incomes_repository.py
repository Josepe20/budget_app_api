from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.api.BUDGET.incomes.incomes_model import Incomes
from app.api.BUDGET.budgets.budget_model import Budget


class IncomeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_income(self, income: Incomes):
        self.db.add(income)
        self.db.commit()
        self.db.refresh(income)
        return income

    def update_income(self, income_id: int, new_data: dict):
        income = self.db.query(Incomes).filter(Incomes.income_id == income_id).first()
        if income:
            for key, value in new_data.items():
                setattr(income, key, value)
            self.db.commit()
            self.db.refresh(income)
        return income

    def delete_income(self, income_id: int):
        income = self.db.query(Incomes).filter(Incomes.income_id == income_id).first()
        if income:
            self.db.delete(income)
            self.db.commit()
        return income

    def get_income_by_id(self, income_id: int):
        return self.db.query(Incomes).filter(Incomes.income_id == income_id).first()

    def get_user_incomes(self, user_id: int):
        return self.db.query(Incomes).join(Budget).filter(Budget.user_id == user_id).all()

    def get_user_active_incomes(self, user_id: int, current_month: int, current_year: int):
        return self.db.query(Incomes).join(Budget).filter(
            Budget.user_id == user_id,
            extract('month', Budget.created_at) == current_month,
            extract('year', Budget.created_at) == current_year
        ).all()

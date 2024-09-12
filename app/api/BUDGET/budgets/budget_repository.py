from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.api.BUDGET.budgets.budget_model import Budget
from app.api.BUDGET.budgets.budget_schema import BudgetResponse


class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[BudgetResponse]:
        budgets = self.db.query(Budget).all()
        return [BudgetResponse.model_validate(budget) for budget in budgets]

    def get_all_by_user_id(self, user_id: int) -> list[BudgetResponse]:
        budgets = self.db.query(Budget).filter(Budget.user_id == user_id).all()
        return [BudgetResponse.model_validate(budget) for budget in budgets]
    
    def get_budget_by_id(self, budget_id: int) -> Budget:
        return self.db.query(Budget).filter(Budget.budget_id == budget_id).first()
    
    def get_budget_by_user_and_month(self, user_id: int, month: int, year: int) -> Budget:
        return self.db.query(Budget).filter(
            Budget.user_id == user_id,
            extract('month', Budget.created_at) == month,
            extract('year', Budget.created_at) == year
        ).first()

    def create_budget(self, budget: Budget) -> Budget:
        self.db.add(budget)
        self.db.commit()
        self.db.refresh(budget)
        return BudgetResponse.model_validate(budget)
    
    def update_budget(self, budget: Budget) -> Budget:
        self.db.commit()
        self.db.refresh(budget)
        return BudgetResponse.model_validate(budget)
    
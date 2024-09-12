from fastapi import APIRouter
from app.api.BUDGET.budgets import budget_router
from app.api.BUDGET.incomes import incomes_router
from app.api.BUDGET.expenses import expenses_router
from app.api.BUDGET.category_expenses import category_exp_router

router = APIRouter()

router.include_router(budget_router.router, prefix="/budgets", tags=["budget"])
router.include_router(incomes_router.router, prefix="/incomes", tags=["incomes"])
router.include_router(expenses_router.router, prefix="/expenses", tags=["expenses"])
router.include_router(category_exp_router.router, prefix="/categories", tags=["categories"])
from fastapi import APIRouter
from api.AUTH.users import users_router
from api.BUDGET.budgets import budget_router
from api.BUDGET.incomes import incomes_router
from app.router.budget import expenses_router

router = APIRouter()

router.include_router(users_router.router, prefix="/users", tags=["users"])
router.include_router(budget_router.router, prefix="/budgets", tags=["budget"])
router.include_router(incomes_router.router, prefix="/incomes", tags=["incomes"])
router.include_router(expenses_router.router, prefix="/expenses", tags=["expenses"])


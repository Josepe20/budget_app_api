from fastapi import APIRouter
from app.router.users import users_router
from app.router.budget import budget_router

router = APIRouter()

router.include_router(users_router.router, prefix="/users", tags=["users"])
router.include_router(budget_router.router, prefix="/budgets", tags=["budget"])


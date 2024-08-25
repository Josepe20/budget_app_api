from fastapi import APIRouter
from router.users import users_router
from router.budget import budget_router

router = APIRouter()

router.include_router(users_router.router, prefix="/users", tags=["users"])
router.include_router(budget_router.router, prefix="/budget", tags=["budget"])


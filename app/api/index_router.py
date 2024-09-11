from fastapi import APIRouter
from app.api.AUTH import auth_index
from app.api.BUDGET import budget_index

router = APIRouter()

router.include_router(auth_index.router)
router.include_router(budget_index.router)


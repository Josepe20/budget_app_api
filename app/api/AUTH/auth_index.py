from fastapi import APIRouter
from app.api.AUTH.users import users_router

router = APIRouter()

router.include_router(users_router.router, prefix="/users", tags=["users"])
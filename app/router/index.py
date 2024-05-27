from fastapi import APIRouter
from app.router.routers import users

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])

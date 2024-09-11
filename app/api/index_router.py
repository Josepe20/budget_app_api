from fastapi import APIRouter
from app.api.AUTH import auth_index

router = APIRouter()

router.include_router(auth_index.router)


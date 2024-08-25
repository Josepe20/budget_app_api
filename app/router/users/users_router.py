from fastapi import APIRouter, Depends, HTTPException
from app.views.users import users_view as user_views
from app.schemas.users import users_schema as user_schemas
from app.schemas import general_schema as general_schemas
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.get("/")
def user_home():
    return "Hello Users"

@router.post("/register")
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db_session)):
    return user_views.register_user(user, db)

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    return user_views.login_user(form_data, db)

@router.post("/logout")
def logout_user():
    return user_views.logout_user()

@router.post("/refresh")
def refresh_token(data: dict, db: Session = Depends(get_db_session)):
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token is missing")
    return user_views.refresh_token(refresh_token, db)

@router.get("/activate/{user_id}")
def activate_account(user_id: int, db: Session = Depends(get_db_session)):
    return user_views.activate_account(user_id, db)

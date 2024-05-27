from fastapi import APIRouter, Depends
from app.views import users as user_views
from app.schemas import users as user_schemas
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.get("/")
def user_home():
    return "Hello Users"

@router.post("/register", response_model=user_schemas.UserResponse)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db_session)):
    return user_views.register_user(user, db)

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    return user_views.login_user(form_data, db)

@router.post("/logout")
def logout_user():
    return user_views.logout_user()

@router.get("/activate/{email_token}")
def activate_account(email_token: str, db: Session = Depends(get_db_session)):
    return user_views.activate_account(email_token, db)

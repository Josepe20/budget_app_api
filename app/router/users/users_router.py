from fastapi import APIRouter, Depends, HTTPException, status
from app.views.users import users_view as user_views
from app.schemas.users.users_schema import UserCreate, UserResponse
from app.functions.api_response import standard_response
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.response_schema import StandardResponse


router = APIRouter()


@router.get("/")
def user_home():
    return "Hello Users"

@router.post("/register", response_model=StandardResponse[UserResponse])
def register_user(user: UserCreate, db: Session = Depends(get_db_session)):
    user_registered, is_new = user_views.register_user(user, db)
    
    if not is_new:
        return standard_response(status.HTTP_200_OK, "Email already registered", user_registered, pydantic_model=UserResponse)

    return standard_response(status.HTTP_201_CREATED, "User registered successfully", user_registered, pydantic_model=UserResponse)      
   

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    tokens_user_logged = user_views.login_user(form_data, db)
    return standard_response(status.HTTP_200_OK, "Login successful", tokens_user_logged)


@router.post("/refresh")
def refresh_token(data: dict, db: Session = Depends(get_db_session)):
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token is missing")
    
    tokens_refreshed = user_views.refresh_token(refresh_token, db)
    return standard_response(status.HTTP_200_OK, "Token refreshed successfully", tokens_refreshed)
    

@router.get("/activate/{user_id}")
def activate_account(user_id: int, db: Session = Depends(get_db_session)):
    response_message = user_views.activate_account(user_id, db)
    return standard_response(status.HTTP_200_OK, response_message)


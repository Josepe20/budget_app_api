from fastapi import APIRouter, Depends, HTTPException, status
from app.api.AUTH.users import users_view as user_views
from app.api.AUTH.users.users_schema import UserCreate, UserResponse, TokenBase, LoginResponse
from app.common.functions.api_response import standard_response
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from fastapi.security import OAuth2PasswordRequestForm
from app.common.schemas.response_schema import StandardResponse


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
   

@router.post("/login", response_model=StandardResponse[LoginResponse])
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    tokens_user_logged = user_views.login_user(form_data, db)
    return standard_response(status.HTTP_200_OK, "Login successful", tokens_user_logged)


@router.post("/refresh", response_model=StandardResponse[TokenBase])
def refresh_token(data: dict, db: Session = Depends(get_db_session)):
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token is missing")
    
    tokens_refreshed = user_views.refresh_token(refresh_token, db)
    return standard_response(status.HTTP_200_OK, "Token refreshed successfully", tokens_refreshed)
    

@router.get("/activate/{user_id}", response_model=StandardResponse[UserResponse])
def activate_account(user_id: int, db: Session = Depends(get_db_session)):
    user_activated = user_views.activate_account(user_id, db)
    return standard_response(status.HTTP_200_OK, "User activated succesfully", user_activated, pydantic_model=UserResponse)


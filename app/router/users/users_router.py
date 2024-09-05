from fastapi import APIRouter, Depends, HTTPException, status
from app.views.users import users_view as user_views
from app.schemas.users import users_schema as user_schemas
from app.functions.api_response import standard_response
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.get("/")
def user_home():
    return "Hello Users"

@router.post("/register")
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db_session)):
    try: 
        user_registered = user_views.register_user(user, db)
        return standard_response(status.HTTP_201_CREATED, "User registered successfully", user_registered)
    except HTTPException as e:
        print("HTTPException: ", e)
        return standard_response(status=e.status_code, message=str(e.detail))
    except Exception as e:
        print("Exception: ", e)
        return standard_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))
        

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    try:
        tokens_user_logged = user_views.login_user(form_data, db)
        return standard_response(status.HTTP_200_OK, "Login successful", tokens_user_logged)
    except HTTPException as e:
        return standard_response(status=e.status_code, message=str(e.detail))
    except Exception as e:
        return standard_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


@router.post("/refresh")
def refresh_token(data: dict, db: Session = Depends(get_db_session)):
    try:
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token is missing")
        
        tokens_refreshed = user_views.refresh_token(refresh_token, db)
        return standard_response(status.HTTP_200_OK, "Token refreshed successfully", tokens_refreshed)
    except HTTPException as e:
        return standard_response(status=e.status_code, message=str(e.detail))
    except Exception as e:
        return standard_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))
    

@router.get("/activate/{user_id}")
def activate_account(user_id: int, db: Session = Depends(get_db_session)):
    try:
        response_message = user_views.activate_account(user_id, db)
        return standard_response(status.HTTP_200_OK, response_message)
    except HTTPException as e:
        return standard_response(status=e.status_code, message=str(e.detail))
    except Exception as e:
        return standard_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

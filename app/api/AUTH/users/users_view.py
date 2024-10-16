from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.AUTH.users.users_schema import UserCreate, UserResponse, LoginResponse, TokenBase
from app.api.AUTH.users.users_repository import UserRepository
from app.api.AUTH.users import user_model as user_models
from app.common.functions.get_obj_or_404 import get_object_or_404, get_list_or_404
from app.dependencies import get_db_session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> dict:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode({"sub": data["sub"]}, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token
    }


def register_user(user: UserCreate, db: Session = Depends(get_db_session)):
    user_repository = UserRepository(db)

    db_user = user_repository.get_user_by_email(user.email)
    if db_user:
        return db_user, False
    
    hashed_password = get_password_hash(user.password)
    new_user = user_models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        is_active=True,
        is_verified=True
    )
    created_user = user_repository.create_user(new_user)

    return created_user, True


def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)) -> LoginResponse:
    user_repository = UserRepository(db)

    user = user_repository.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Account not verified")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    sub_contennt = f"{user.user_id}-{user.username}"
    tokens = create_access_token(data={"sub": sub_contennt}, expires_delta=access_token_expires)

    return {
        "access_token": tokens["access_token"], 
        "refresh_token": tokens["refresh_token"], 
        "token_type": "bearer"
    }


def refresh_token(refresh_token: str, db: Session = Depends(get_db_session)) -> TokenBase:
    try:
        user_repository = UserRepository(db)
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        sub_content = payload.get("sub")

        if not sub_content:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        id_user_token, username_token = sub_content.split("-")
        print(username_token)
        user = user_repository.get_user_by_id(id_user_token)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(data={"sub": sub_content}, expires_delta=access_token_expires)
        
        return {
            "access_token": new_access_token["access_token"],
            "token_type": "bearer"
        }
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")

    
def activate_account(user_id: int, db: Session = Depends(get_db_session)) -> UserResponse:
    user_repository = UserRepository(db)

    user = get_object_or_404(user_repository.get_user_by_id(user_id), "User Not Found")

    user.is_verified = True
    user_repository.update_user(user)
    return user


def get_user_by_id(user_id: int, db: Session = Depends(get_db_session)) -> UserResponse:
    user_repository = UserRepository(db)

    user = get_object_or_404(user_repository.get_user_by_id(user_id), "User Not Found")   
    return user  


def get_user_by_email(user_email: str, db: Session = Depends(get_db_session)) -> UserResponse:
    user_repository = UserRepository(db)

    user = get_object_or_404(user_repository.get_user_by_email(user_email), "User Not Found")   
    return user  


def update_user_email_by_id(user_id: int, new_email:str, db: Session = Depends(get_db_session)) -> UserResponse:
    user_repository = UserRepository(db)

    user = get_object_or_404(user_repository.get_user_by_id(user_id), "User Not Found")
    user.email = new_email
    user_repository.update_user(user)
    
    return user


def update_user_password_by_id(user_id: int, new_password: str, db: Session = Depends(get_db_session)) -> UserResponse:
    user_repository = UserRepository(db)

    user =  get_object_or_404(user_repository.get_user_by_id(user_id), "User Not Found")
    
    hashed_password = get_password_hash(new_password)
    user.password = hashed_password
    user_repository.update_user(user)
    
    return user


def delete_user_by_id(user_id: int, db: Session = Depends(get_db_session)) -> UserResponse:
    user_repository = UserRepository(db)

    user_to_delete = get_object_or_404(user_repository.get_user_by_id(user_id), "User Not Found")
    
    deleted_user = user_repository.deleted_user(user_to_delete.user_id)
    return deleted_user


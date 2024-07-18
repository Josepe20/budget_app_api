from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas import users as user_schemas
from app.models import users as user_models
from app.dependencies import get_db_session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import uuid
from app.functions.emails import send_account_activation_email
from app.functions.api_response import standard_response
from typing import Optional
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.now(datetime.UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode({"sub": data["sub"]}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/register", response_model=user_schemas.UserResponse)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db_session)):
    db_user = db.query(user_models.User).filter(user_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    email_token = str(uuid.uuid4())
    db_user = user_models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        is_active=True,
        is_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    send_account_activation_email(user.email, db_user.id)
    return standard_response(status.HTTP_201_CREATED, "User registered successfully", db_user)

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    user = db.query(user_models.User).filter(user_models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Account not verified")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    sub_contennt = f"{user.id}-{user.username}"
    tokens = create_access_token(data={"sub": sub_contennt}, expires_delta=access_token_expires)

    data_response = {
        "access_token": tokens["access_token"], 
        "refresh_token": tokens["refresh_token"], 
        "token_type": "bearer"
        }
    return standard_response(status.HTTP_200_OK, "Login successful", data_response)

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db_session)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        sub_content = payload.get("sub")
        if not sub_content:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        id_user, username = sub_content.split("-")
        user = db.query(user_models.User).filter(user_models.User.id == id_user, user_models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(data={"sub": sub_content}, expires_delta=access_token_expires)

        data_response = {
            "access_token": new_access_token["access_token"], 
            "token_type": "bearer"
        }
        return standard_response(status.HTTP_200_OK, "Token refreshed successfully", data_response)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    

@router.get("/activate/{user_id}")
def activate_account(user_id: int, db: Session = Depends(get_db_session)):
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID")
    user.is_verified = True
    db.commit()
    return standard_response(status.HTTP_200_OK, "Account successfully activated")



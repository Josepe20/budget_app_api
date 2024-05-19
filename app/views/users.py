from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import users as user_schemas
from models import users as user_models
from dependencies import get_db_session


def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db_session)):
    db_user = user_models.User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int, db: Session = Depends(get_db_session)):
    db_user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

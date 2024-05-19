from fastapi import APIRouter
from views import users as user_views
from schemas import users as user_schemas

router = APIRouter()

@router.get("/")
def hello_user():
    return "Hola Users"

@router.post("/create_user", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(user_views.get_db_session)):
    return user_views.create_user(user, db)

@router.get("/{user_id}", response_model=user_schemas.User)
def get_user(user_id: int, db: Session = Depends(user_views.get_db_session)):
    return user_views.get_user(user_id, db)

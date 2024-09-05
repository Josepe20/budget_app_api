import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db_session
from sqlalchemy import create_engine
from app.models.users.users import User
from sqlalchemy.orm import sessionmaker
from app.database import Base
from decouple import config

USERNAME = config('USERNAME_DB')
PASSWORD = config('PASSWORD_DB')
HOST = config('HOST_DB')
PORT = config('PORT_DB')
DB_NAME = config('DATABASE_NAME')

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}" 

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_session] = override_get_db_session

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "josechay_test",
        "email": "moalgeda@gmail.com",
        "password": "123"
    }


def clear_user_in_db():
    db = TestingSessionLocal()
    db.query(User).filter(User.username == test_user["username"]).delete()
    db.commit()
    db.close()


def test_register_user(test_user):
    try:
        # Primer intento: el usuario debería registrarse correctamente
        response = client.post("/users/register", json=test_user)
        assert response.status_code == 201
        assert response.json()["message"] == "User registered successfully"
    except AssertionError:
        # Si el usuario ya existe, se captura el error esperado
        assert response.status_code == 200
        assert response.json()["message"] == "Email already registered"
    
    # Intentar de nuevo para asegurarse de que en el segundo intento ya existe el email
    response = client.post("/users/register", json=test_user)
    assert response.status_code == 200
    assert response.json()["message"] == "Email already registered"


def test_login_user(test_user):
    # Aseguramos que el usuario ya está registrado
    client.post("/users/register", json=test_user)

     # Intentamos hacer login con el usuario registrado
    response = client.post("/users/login", data={"username": test_user["username"], "password": test_user["password"]})
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert "access_token" in response.json()["data"]
    

def test_refresh_token(test_user):
     # Registramos al usuario y obtenemos el token de acceso y de refresco
    client.post("/users/register", json=test_user)
    login_response = client.post("/users/login", data={"username": test_user["username"], "password": test_user["password"]})
    refresh_token = login_response.json()["data"]["refresh_token"]

    # Intentamos refrescar el token
    refresh_response = client.post("/users/refresh", json={"refresh_token": refresh_token})
    assert refresh_response.status_code == 200
    assert refresh_response.json()["message"] == "Token refreshed successfully"
    assert "access_token" in refresh_response.json()["data"]

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.api.BUDGET.budgets.budget_model import Budget
from app.api.AUTH.users.user_model import User
from app.api.BUDGET.incomes.incomes_model import Incomes
from decouple import config
from jose import jwt

# Configuration algoritm 
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

# Configuration DB
USERNAME = config('USERNAME_DB')
PASSWORD = config('PASSWORD_DB')
HOST = config('HOST_DB')
PORT = config('PORT_DB')
DB_NAME = config('DATABASE_NAME')

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}" 

# Setup database session for testing
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

# Fixtures
@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }

@pytest.fixture
def test_budget(test_user):
    # Ensure the user is created before creating a budget
    client.post("/api/users/register", json=test_user)
    user_response = client.post("/api/users/login", data={"username": test_user["username"], "password": test_user["password"]})
    
    # Extract user_id from login access token 
    access_token = user_response.json()["data"]["access_token"]
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    sub_content = decoded_token.get("sub")
    user_id = sub_content.split("-")[0] 

    
    # Create a budget for the user
    budget_data = {
        "user_id": user_id,
        "total_income": 0,
        "total_expense": 0
    }
    create_budget_response = client.post("/api/budgets/create", json=budget_data)
    return create_budget_response.json()["data"]

@pytest.fixture
def test_income(test_budget):
    return {
        "budget_id": test_budget["budget_id"],
        "amount": 1000.0,
        "income_name": "Test Income"
    }

# Helper function to clear test data from the DB
def clear_income_in_db(income_id: int):
    db = TestingSessionLocal()
    db.query(Incomes).filter(Incomes.income_id == income_id).delete()
    db.commit()
    db.close()

#################### Test cases ########################

def test_create_income(test_income):
    response = client.post("/api/incomes/create", json=test_income)
    assert response.status_code == 201
    assert response.json()["message"] == "income created succesfully"
    assert response.json()["data"]["income_name"] == "Test Income"


def test_update_income(test_income):
    # First create the income
    create_response = client.post("/api/incomes/create", json=test_income)
    income_id = create_response.json()["data"]["income_id"]

    # Update the income
    updated_data = {
        "budget_id": test_income["budget_id"],
        "amount": 2000.0,
        "income_name": "Updated Income"
    }
    response = client.put(f"/api/incomes/update/{income_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["message"] == "income updated successfully"
    assert response.json()["data"]["amount"] == 2000.0

    # Clean up the created income
    clear_income_in_db(income_id)


def test_delete_income(test_income):
    # First create the income
    create_response = client.post("/api/incomes/create", json=test_income)
    income_id = create_response.json()["data"]["income_id"]

    # Delete the income
    response = client.delete(f"/api/incomes/delete/{income_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "income deleted succesfully"


def test_get_income_by_id(test_income):
    # First create the income
    create_response = client.post("/api/incomes/create", json=test_income)
    income_id = create_response.json()["data"]["income_id"]

    # Get the income by ID
    response = client.get(f"/api/incomes/{income_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "income found"
    assert response.json()["data"]["income_name"] == test_income["income_name"]

    # Clean up the created income
    clear_income_in_db(income_id)


def test_get_user_incomes(test_user, test_budget, test_income):
    # First create the income
    client.post("/api/incomes/create", json=test_income)

    # Get all incomes for the user
    user_response = client.post("/api/users/login", data={"username": test_user["username"], "password": test_user["password"]})  
    # Extract user_id from login access token 
    access_token = user_response.json()["data"]["access_token"]
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    sub_content = decoded_token.get("sub")
    user_id = sub_content.split("-")[0] 

    response = client.get(f"/api/incomes/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "incomes found"
    assert len(response.json()["data"]) > 0


def test_get_user_active_incomes(test_user, test_budget, test_income):
    # First create the income
    client.post("/api/incomes/create", json=test_income)

    # Get active incomes for the user
    user_response = client.post("/api/users/login", data={"username": test_user["username"], "password": test_user["password"]})  
    # Extract user_id from login access token 
    access_token = user_response.json()["data"]["access_token"]
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    sub_content = decoded_token.get("sub")
    user_id = sub_content.split("-")[0] 
    
    response = client.get(f"/api/incomes/user/{user_id}/active")
    assert response.status_code == 200
    assert response.json()["message"] == "incomes found"
    assert len(response.json()["data"]) > 0
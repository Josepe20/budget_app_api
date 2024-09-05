import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.budget.budget import Budget
from app.models.users.users import User
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
        "username": "testuser_budget",
        "email": "testuser_budget@gmail.com",
        "password": "123"
    }

def clear_user_in_db():
    db = TestingSessionLocal()
    db.query(User).filter(User.username == test_user["username"]).delete()
    db.commit()
    db.close()

@pytest.fixture
def test_budget(test_user):
    client.post("/users/register", json=test_user)   
    user_response = client.post("/users/login", data={"username": test_user["username"], "password": test_user["password"]})
    
    # Extract user_id from login access token 
    access_token = user_response.json()["data"]["access_token"]
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    sub_content = decoded_token.get("sub")
    user_id = sub_content.split("-")[0] 

    return {
        "user_id": user_id,
        "total_income": 1000.0,
        "total_expense": 500.0
    }


# Helper function to clear test data from the DB
def clear_budget_in_db(user_id: int):
    db = TestingSessionLocal()
    db.query(Budget).filter(Budget.user_id == user_id).delete()
    db.commit()
    db.close()

# Test Cases

def test_create_budget(test_budget):
    # First attempt: Create the budget
    response = client.post("/budgets/create-budget", json=test_budget)

    # Handle both possible cases:
    if response.status_code == 201:
        assert response.json()["message"] == "Budget created successfully"
    elif response.status_code == 200:
        assert response.json()["message"] == "Budget already exist"
    else:
        # Fail the test if neither 201 nor 200 is returned
        pytest.fail(f"Unexpected status code: {response.status_code}")
    
    # Second attempt: The budget already exists for this month, so it should return 200
    response = client.post("/budgets/create-budget", json=test_budget)
    assert response.status_code == 200
    assert response.json()["message"] == "Budget already exist"



def test_get_budget_by_id(test_budget):
    # Create a budget first
    create_response = client.post("/budgets/create-budget", json=test_budget)
    budget_id = create_response.json()["data"]["budget_id"]

    # Fetch the budget by ID
    response = client.get(f"/budgets/{budget_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Budget found"
    assert response.json()["data"]["budget_id"] == budget_id


def test_get_all_budgets_by_user(test_budget):
    # Ensure a budget exists for the test user
    client.post("/budgets/create-budget", json=test_budget)

    # Fetch all budgets for the user
    user_id = test_budget["user_id"]
    response = client.get(f"/budgets/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Budgets fetched successfully"
    assert len(response.json()["data"]) > 0

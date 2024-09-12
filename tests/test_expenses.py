import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.api.BUDGET.budgets.budget_model import Budget
from app.api.AUTH.users.user_model import User
from app.api.BUDGET.expenses.expenses_model import Expenses
from app.api.BUDGET.category_expenses.category_exp_model import CategoryExpenses
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
def test_category_expense():
    # Assuming you have pre-inserted categories in your database
    return 1  # Replace with the actual category_id (1, 2, or 3)

@pytest.fixture
def test_expense(test_budget, test_category_expense):
    return {
        "budget_id": test_budget["budget_id"],
        "category_expense_id": test_category_expense,
        "amount": 500.0,
        "expense_name": "Test Expense"
    }

# Helper function to clear test data from the DB
def clear_expense_in_db(expense_id: int):
    db = TestingSessionLocal()
    db.query(Expenses).filter(Expenses.expense_id == expense_id).delete()
    db.commit()
    db.close()

#################### Test cases ########################

def test_create_expense(test_expense):
    response = client.post("/api/expenses/create", json=test_expense)
    assert response.status_code == 201
    assert response.json()["message"] == "expense created succesfully"
    assert response.json()["data"]["expense_name"] == "Test Expense"


def test_update_expense(test_expense):
    # First create the expense
    create_response = client.post("/api/expenses/create", json=test_expense)
    expense_id = create_response.json()["data"]["expense_id"]

    # Update the expense
    updated_data = {
        "budget_id": test_expense["budget_id"],
        "category_expense_id": test_expense["category_expense_id"],
        "amount": 750.0,
        "expense_name": "Updated Expense"
    }
    response = client.put(f"/api/expenses/update/{expense_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["message"] == "expense updated successfully"
    assert response.json()["data"]["amount"] == 750.0

    # Clean up the created expense
    clear_expense_in_db(expense_id)


def test_delete_expense(test_expense):
    # First create the expense
    create_response = client.post("/api/expenses/create", json=test_expense)
    expense_id = create_response.json()["data"]["expense_id"]

    # Delete the expense
    response = client.delete(f"/api/expenses/delete/{expense_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "expense deleted succesfully"


def test_get_expense_by_id(test_expense):
    # First create the expense
    create_response = client.post("/api/expenses/create", json=test_expense)
    expense_id = create_response.json()["data"]["expense_id"]

    # Get the expense by ID
    response = client.get(f"/api/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "expense found"
    assert response.json()["data"]["expense_name"] == test_expense["expense_name"]

    # Clean up the created expense
    clear_expense_in_db(expense_id)


def test_get_user_expenses(test_user, test_budget, test_expense):
    # First create the expense
    client.post("/api/expenses/create", json=test_expense)

    # Get all expenses for the user
    user_response = client.post("/api/users/login", data={"username": test_user["username"], "password": test_user["password"]})
    access_token = user_response.json()["data"]["access_token"]
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    sub_content = decoded_token.get("sub")
    user_id = sub_content.split("-")[0]

    response = client.get(f"/api/expenses/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "expenses found"
    assert len(response.json()["data"]) > 0


def test_get_user_active_expenses(test_user, test_budget, test_expense):
    # First create the expense
    client.post("/api/expenses/create", json=test_expense)

    # Get active expenses for the user
    user_response = client.post("/api/users/login", data={"username": test_user["username"], "password": test_user["password"]})
    access_token = user_response.json()["data"]["access_token"]
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    sub_content = decoded_token.get("sub")
    user_id = sub_content.split("-")[0]

    response = client.get(f"/api/expenses/user/{user_id}/active")
    assert response.status_code == 200
    assert response.json()["message"] == "expenses found"
    assert len(response.json()["data"]) > 0


def test_get_user_expenses_by_category(test_user, test_budget, test_expense, test_category_expense):
    # First create the expense
    client.post("/api/expenses/create", json=test_expense)

    # Get all expenses for the user by category
    user_response = client.post("/api/users/login", data={"username": test_user["username"], "password": test_user["password"]})
    access_token = user_response.json()["data"]["access_token"]
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    sub_content = decoded_token.get("sub")
    user_id = sub_content.split("-")[0]

    response = client.get(f"/api/expenses/user/{user_id}/category/{test_category_expense}")
    assert response.status_code == 200
    assert response.json()["message"] == "expenses found"
    assert len(response.json()["data"]) > 0
    assert response.json()["data"][0]["category_expense_id"] == test_category_expense
    

def test_get_user_active_expenses_by_category(test_user, test_budget, test_expense, test_category_expense):
    # First create the expense
    client.post("/api/expenses/create", json=test_expense)

    # Get active expenses for the user by category
    user_response = client.post("/api/users/login", data={"username": test_user["username"], "password": test_user["password"]})
    access_token = user_response.json()["data"]["access_token"]
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    sub_content = decoded_token.get("sub")
    user_id = sub_content.split("-")[0]

    response = client.get(f"/api/expenses/user/{user_id}/category/{test_category_expense}/active")
    assert response.status_code == 200
    assert response.json()["message"] == "expenses found"
    assert len(response.json()["data"]) > 0
    assert response.json()["data"][0]["category_expense_id"] == test_category_expense


from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.common.functions.api_response import standard_response
from app.api.BUDGET.expenses.expenses_schema import ExpenseCreate, ExpenseResponse
from app.api.BUDGET.expenses import expenses_view
from app.common.schemas.response_schema import StandardResponse


router = APIRouter()


@router.post("/create", response_model=StandardResponse[ExpenseResponse])
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db_session)):
    created_expense = expenses_view.create_expense(expense, db)
    return standard_response(status.HTTP_201_CREATED, "expense created succesfully", created_expense, pydantic_model=ExpenseResponse)   


@router.put("/update/{expense_id}", response_model=StandardResponse[ExpenseResponse])
def update_expense(expense_id: int, expense: ExpenseCreate, db: Session = Depends(get_db_session)):
    updated_expense = expenses_view.update_expense(expense_id, expense.model_dump(), db)
    return standard_response(status.HTTP_200_OK, "expense updated successfully", updated_expense, pydantic_model=ExpenseResponse)  


@router.delete("/delete/{expense_id}", response_model=StandardResponse[ExpenseResponse])
def delete_expense(expense_id: int, db: Session = Depends(get_db_session)):
    deleted_expense = expenses_view.delete_expense(expense_id, db)
    return standard_response(status.HTTP_200_OK, "expense deleted succesfully", deleted_expense, pydantic_model=ExpenseResponse)


@router.get("/{expense_id}", response_model=StandardResponse[ExpenseResponse])
def get_expense_by_id(expense_id: int, db: Session = Depends(get_db_session)):
    expense_found = expenses_view.get_expense_by_id(expense_id, db)
    return standard_response(status.HTTP_200_OK, "expense found", expense_found, pydantic_model=ExpenseResponse)
    

@router.get("/user/{user_id}", response_model=StandardResponse[list[ExpenseResponse]])
def get_user_expenses(user_id: int, db: Session = Depends(get_db_session)):
    expenses_list = expenses_view.get_user_expenses(user_id, db)
    return standard_response(status.HTTP_200_OK, "expenses found", expenses_list, pydantic_model=ExpenseResponse)
    

@router.get("/user/{user_id}/active", response_model=StandardResponse[list[ExpenseResponse]])
def get_user_active_expenses(user_id: int, db: Session = Depends(get_db_session)):
    expenses_list = expenses_view.get_user_active_expenses(user_id, db)
    return standard_response(status.HTTP_200_OK, "expenses found", expenses_list, pydantic_model=ExpenseResponse)


@router.get("/user/{user_id}/category/{category_id}", response_model=StandardResponse[list[ExpenseResponse]])
def get_user_expenses_by_category(user_id: int, category_id: int, db: Session = Depends(get_db_session)):
    expenses_list = expenses_view.get_user_expenses_by_category(user_id, category_id, db)
    return standard_response(status.HTTP_200_OK, "expenses found", expenses_list, pydantic_model=ExpenseResponse)


@router.get("/user/{user_id}/category/{category_id}/active", response_model=StandardResponse[list[ExpenseResponse]])
def get_user_active_expenses_by_category(user_id: int, category_id: int, db: Session = Depends(get_db_session)):
    expenses_list = expenses_view.get_user_expenses_by_category(user_id, category_id, db)
    return standard_response(status.HTTP_200_OK, "expenses found", expenses_list, pydantic_model=ExpenseResponse)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.functions.api_response import standard_response
from app.schemas.budget.income_schema import IncomeCreate 
from app.views.budget import incomes_view

router = APIRouter()


@router.post("/create")
def create_income(income: IncomeCreate, db: Session = Depends(get_db_session)):
    created_income = incomes_view.create_income(income, db)
    return standard_response(status.HTTP_201_CREATED, "income created succesfully", created_income)   


@router.put("/update/{income_id}")
def update_income(income_id: int, income: IncomeCreate, db: Session = Depends(get_db_session)):
    updated_income = incomes_view.update_income(income_id, income.model_dump(), db)
    return standard_response(status.HTTP_200_OK, "income updated successfully", updated_income)
    

@router.delete("/delete/{income_id}")
def delete_income(income_id: int, db: Session = Depends(get_db_session)):
    deleted_message = incomes_view.delete_income(income_id, db)
    return standard_response(status.HTTP_200_OK, "income deleted succesfully", deleted_message)
    

@router.get("/{income_id}")
def get_income_by_id(income_id: int, db: Session = Depends(get_db_session)):
    income_found = incomes_view.get_income_by_id(income_id, db)
    return standard_response(status.HTTP_200_OK, "income found", income_found)
    

@router.get("/user/{user_id}")
def get_user_incomes(user_id: int, db: Session = Depends(get_db_session)):
    incomes_list = incomes_view.get_user_incomes(user_id, db)
    return standard_response(status.HTTP_200_OK, "incomes found", incomes_list)
    

@router.get("/user/{user_id}/active")
def get_user_active_incomes(user_id: int, db: Session = Depends(get_db_session)):
    incomes_list = incomes_view.get_user_active_incomes(user_id, db)
    return standard_response(status.HTTP_200_OK, "incomes found", incomes_list)

    
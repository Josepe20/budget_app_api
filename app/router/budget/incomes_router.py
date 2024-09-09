from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.functions.api_response import standard_response
from app.schemas.budget.income_schema import IncomeCreate, IncomeResponse
from app.views.budget import incomes_view
from app.schemas.response_schema import StandardResponse


router = APIRouter()


@router.post("/create", response_model=StandardResponse[IncomeResponse])
def create_income(income: IncomeCreate, db: Session = Depends(get_db_session)):
    created_income = incomes_view.create_income(income, db)
    return standard_response(status.HTTP_201_CREATED, "income created succesfully", created_income, pydantic_model=IncomeResponse)   


@router.put("/update/{income_id}", response_model=StandardResponse[IncomeResponse])
def update_income(income_id: int, income: IncomeCreate, db: Session = Depends(get_db_session)):
    updated_income = incomes_view.update_income(income_id, income.model_dump(), db)
    return standard_response(status.HTTP_200_OK, "income updated successfully", updated_income, pydantic_model=IncomeResponse)
    

@router.delete("/delete/{income_id}", response_model=StandardResponse[IncomeResponse])
def delete_income(income_id: int, db: Session = Depends(get_db_session)):
    deleted_message = incomes_view.delete_income(income_id, db)
    return standard_response(status.HTTP_200_OK, "income deleted succesfully", deleted_message, pydantic_model=IncomeResponse)
    

@router.get("/{income_id}", response_model=StandardResponse[IncomeResponse])
def get_income_by_id(income_id: int, db: Session = Depends(get_db_session)):
    income_found = incomes_view.get_income_by_id(income_id, db)
    return standard_response(status.HTTP_200_OK, "income found", income_found, pydantic_model=IncomeResponse)
    

@router.get("/user/{user_id}", response_model=StandardResponse[list[IncomeResponse]])
def get_user_incomes(user_id: int, db: Session = Depends(get_db_session)):
    incomes_list = incomes_view.get_user_incomes(user_id, db)
    return standard_response(status.HTTP_200_OK, "incomes found", incomes_list, pydantic_model=IncomeResponse)
    

@router.get("/user/{user_id}/active", response_model=StandardResponse[list[IncomeResponse]])
def get_user_active_incomes(user_id: int, db: Session = Depends(get_db_session)):
    incomes_list = incomes_view.get_user_active_incomes(user_id, db)
    return standard_response(status.HTTP_200_OK, "incomes found", incomes_list, pydantic_model=IncomeResponse)

    
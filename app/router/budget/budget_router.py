from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.functions.api_response import standard_response
from app.schemas.budget.budget_schema import BudgetCreate, BudgetResponse
from app.views.budget import budget_view


router = APIRouter()


@router.get("/")
def get_all_budgets(db: Session = Depends(get_db_session)):
    budget_list = budget_view.get_all_budgets(db)
    return standard_response(status.HTTP_200_OK, "Budgets fetched successfully", budget_list)   
    

@router.get("/user/{user_id}")
def get_all_user_budgets(user_id: int, db: Session = Depends(get_db_session)):
    budget_list = budget_view.get_all_budgets_by_user(user_id, db)
    return standard_response(status.HTTP_200_OK, "Budgets fetched successfully", budget_list)
    

@router.get("/{budget_id}")
def get_budget_by_id(budget_id: int, db: Session = Depends(get_db_session)):
    budget_found = budget_view.get_budget_by_id(budget_id, db)
    return standard_response(status.HTTP_200_OK, "Budget found", budget_found)
    

@router.post("/create-budget")
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db_session)):
    budget_created, is_new = budget_view.create_budget(budget, db)
    
    if not is_new:
        return standard_response(status.HTTP_200_OK, "Budget already exist", budget_created)

    return standard_response(status.HTTP_201_CREATED, "Budget created successfully", budget_created)     

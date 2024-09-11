from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.common.functions.api_response import standard_response
from app.api.BUDGET.budgets.budget_schema import BudgetCreate, BudgetResponse
from app.api.BUDGET.budgets import budget_view
from app.common.schemas.response_schema import StandardResponse


router = APIRouter()


@router.get("/", response_model=StandardResponse[list[BudgetResponse]])
def get_all_budgets(db: Session = Depends(get_db_session)):
    budget_list = budget_view.get_all_budgets(db)
    return standard_response(status.HTTP_200_OK, "Budgets fetched successfully", budget_list, pydantic_model=BudgetResponse)   
    

@router.get("/user/{user_id}", response_model=StandardResponse[list[BudgetResponse]])
def get_all_user_budgets(user_id: int, db: Session = Depends(get_db_session)):
    budget_list = budget_view.get_all_budgets_by_user(user_id, db)
    return standard_response(status.HTTP_200_OK, "Budgets fetched successfully", budget_list, budget_list, pydantic_model=BudgetResponse)
    

@router.get("/{budget_id}", response_model=StandardResponse[BudgetResponse])
def get_budget_by_id(budget_id: int, db: Session = Depends(get_db_session)):
    budget_found = budget_view.get_budget_by_id(budget_id, db)
    return standard_response(status.HTTP_200_OK, "Budget found", budget_found, pydantic_model=BudgetResponse)
    

@router.post("/create", response_model=StandardResponse[BudgetResponse])
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db_session)):
    budget_created, is_new = budget_view.create_budget(budget, db)
    
    if not is_new:
        return standard_response(status.HTTP_200_OK, "Budget already exist", budget_created, pydantic_model=BudgetResponse)

    return standard_response(status.HTTP_201_CREATED, "Budget created successfully", budget_created, pydantic_model=BudgetResponse)     

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.functions.api_response import standard_response
from app.schemas.budget.budget_schema import BudgetCreate, BudgetResponse
from app.views.budget import budget_view
from app.router.budget.routes import incomes_router, expenses_router


router = APIRouter()
router.include_router(incomes_router.router, prefix="/incomes", tags=["incomes"])
router.include_router(expenses_router.router, prefix="/expenses", tags=["expenses"])


@router.get("/")
def get_all_budgets(db: Session = Depends(get_db_session)):
    try:
        budget_list = budget_view.get_all_budgets(db)
        return standard_response(status.HTTP_200_OK, "Budgets fetched successfully", budget_list)
    except HTTPException as e:
        print("HTTPException:", e)
        return standard_response(status=e.status_code, message=str(e.detail))
    except Exception as e:
        print("Exception:", e)
        return standard_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))
    

@router.get("/user/{user_id}")
def get_all_user_budgets(user_id: int, db: Session = Depends(get_db_session)):
    try:
        budget_list = budget_view.get_all_budgets_by_user(user_id, db)
        return standard_response(status.HTTP_200_OK, "Budgets fetched successfully", budget_list)
    except HTTPException as e:
        print("HTTPException:", e)
        return standard_response(status=e.status_code, message=str(e.detail))
    except Exception as e:
        print("Exception:", e)
        return standard_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


@router.get("/{budget_id}")
def get_budget_by_id(budget_id: int, db: Session = Depends(get_db_session)):
    try:
        budget_found = budget_view.get_budget_by_id(budget_id, db)
        return standard_response(status.HTTP_200_OK, "Budget found", budget_found)
    except HTTPException as e:
        print("HTTPException:", e)
        return standard_response(status=e.status_code, message=str(e.detail))
    except Exception as e:
        print("Exception:", e)
        return standard_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


@router.post("/create-budget")
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db_session)):
    try: 
        budget_created, is_new = budget_view.create_budget(budget, db)
        
        if not is_new:
            return standard_response(status.HTTP_200_OK, "Budget already exist", budget_created)

        return standard_response(status.HTTP_201_CREATED, "Budget created successfully", budget_created) 
    except HTTPException as e:
        print("HTTPException:", e)
        return standard_response(status=e.status_code, message=str(e.detail))
    except Exception as e:
        print("Exception:", e)
        return standard_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


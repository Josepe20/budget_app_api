from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.common.functions.api_response import standard_response
from app.api.BUDGET.category_expenses.category_exp_schema import CategoryExpensesResponse
from app.api.BUDGET.category_expenses import category_exp_view
from app.common.schemas.response_schema import StandardResponse


router = APIRouter()
      

@router.get("/", response_model=StandardResponse[list[CategoryExpensesResponse]])
def get_all_categories(db: Session = Depends(get_db_session)):
    categories_list = category_exp_view.get_all_categories(db)
    return standard_response(status.HTTP_200_OK, "categories found", categories_list, pydantic_model=CategoryExpensesResponse)


@router.get("/{category_id}", response_model=StandardResponse[CategoryExpensesResponse])
def get_category_by_id(category_id: int, db: Session = Depends(get_db_session)):
    category_found = category_exp_view.get_category_by_id(category_id, db)
    return standard_response(status.HTTP_200_OK, "category found", category_found, pydantic_model=CategoryExpensesResponse)
    
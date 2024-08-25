from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.schemas.budget.budget_schema import BudgetCreate, BudgetResponse
from app.views.budget import budget_view
from router.budget.routes import incomes_router, expenses_router


router = APIRouter()
router.include_router(incomes_router.router, prefix="/incomes", tags=["incomes"])
router.include_router(expenses_router.router, prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=list[BudgetResponse])
def get_all_budgets(db: Session = Depends(get_db_session)):
    return budget_view.get_all_budgets(db)


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget_by_id(budget_id: int, db: Session = Depends(get_db_session)):
    return budget_view.get_budget_by_id(budget_id, db)


@router.post("/create-budget", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db_session)):
    return budget_view.create_budget(budget, db)


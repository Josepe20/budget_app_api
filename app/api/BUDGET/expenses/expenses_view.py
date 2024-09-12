from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.api.BUDGET.expenses.expenses_model import Expenses
from app.api.BUDGET.expenses.expenses_schema import ExpenseCreate
from app.api.BUDGET.expenses.expenses_repository import ExpenseRepository
from app.common.functions.validate_active_month import validate_active_month
from app.api.BUDGET.budgets.budget_view import update_budget_totals


def create_expense(expense_data: ExpenseCreate, db: Session):
    expense_repository = ExpenseRepository(db)
    new_expense = Expenses(
        budget_id=expense_data.budget_id,
        category_expense_id=expense_data.category_expense_id,
        expense_name=expense_data.expense_name,
        amount=expense_data.amount, 
        created_at=datetime.now(timezone.utc)
    )

    validate_active_month(new_expense.created_at)

    created_expense = expense_repository.create_expense(new_expense)

    # update the total budget expense
    update_budget_totals(
        budget_id=expense_data.budget_id, 
        type="expense", 
        operation="sum", 
        amount=new_expense.amount, 
        db=db
    )

    # Refresh the object state
    db.refresh(created_expense)
    return created_expense


def update_expense(expense_id: int, expense_data: dict, db: Session):
    expense_repository = ExpenseRepository(db)

    expense_to_update = expense_repository.get_expense_by_id(expense_id)
    if not expense_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    
    validate_active_month(expense_to_update.created_at)

    # Calculate the difference between the old and new value
    difference = expense_data['amount'] - expense_to_update.amount

    updated_expense = expense_repository.update_expense(expense_id, expense_data)

    # update the total budget expense
    update_budget_totals(
        budget_id=updated_expense.budget_id,
        type="expense",
        operation="sum" if difference > 0 else "sub",
        amount=abs(difference),
        db=db
    )

    # Refresh the object state
    db.refresh(updated_expense)
    return updated_expense


def delete_expense(expense_id: int, db: Session):
    expense_repository = ExpenseRepository(db)

    expense_to_delete = expense_repository.get_expense_by_id(expense_id)
    if not expense_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    
    validate_active_month(expense_to_delete.created_at)

    # update the total budget expense
    update_budget_totals(
        budget_id=expense_to_delete.budget_id, 
        type="expense", 
        operation="sub", 
        amount=expense_to_delete.amount, 
        db=db
    )

    deleted_expense = expense_repository.delete_expense(expense_id)
    return deleted_expense


def get_expense_by_id(expense_id: int, db: Session):
    expense_repository = ExpenseRepository(db)
    expense = expense_repository.get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


def get_user_expenses(user_id: int, db: Session):
    expense_repository = ExpenseRepository(db)
    expenses = expense_repository.get_user_expenses(user_id)
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found")
    return expenses


def get_user_active_expenses(user_id: int, db: Session):
    expense_repository = ExpenseRepository(db)
    current_month = datetime.now().month
    current_year = datetime.now().year
    expenses = expense_repository.get_user_active_expenses(user_id, current_month, current_year)
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active expenses found")
    return expenses


def get_user_expenses_by_category(user_id: int, category_id: int, db: Session):
    expense_repository = ExpenseRepository(db)
    expenses = expense_repository.get_user_expenses_by_category(user_id, category_id)
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found")
    return expenses


def get_user_active_expenses_by_category(user_id: int, category_id: int, db: Session):
    expense_repository = ExpenseRepository(db)
    current_month = datetime.now().month
    current_year = datetime.now().year
    expenses = expense_repository.get_user_active_expenses_by_category(user_id, category_id, current_month, current_year)
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active expenses found")
    return expenses
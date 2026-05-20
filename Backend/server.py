from fastapi import FastAPI, HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

app=FastAPI()

class Expense(BaseModel):

    amount: int
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

@app.get("/expense/{expense_date}", response_model=List[Expense])
def get_expense(expense_date:date):
    expense = db_helper.fetch_expenses_for_date(expense_date)
    if expense is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense data from the database")

    return expense

@app.post("/expense/{expense_date}")
def add_or_update_expense(expense_date:date,expense:List[Expense]):
    db_helper.delete_expense_for_date(expense_date)
    for expenses in expense:
        db_helper.insert_expense_for_date(expense_date,expenses.amount,expenses.category,expenses.notes)

    return {"message":"Expense updated successfully"}

@app.post("/analytics/")
def get_analytics(date_range :DateRange):
    data=db_helper.fetch_expense_summary(date_range.start_date,date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database")
    total = sum ([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total']/total)*100 if total!=0 else 0
        breakdown[row['category']] = {
            "total": row["total"],
            "percentage": percentage,
        }
    return breakdown


@app.post("/analytics_by_month/")
def get_analytics_by_month():
    monthly_data=db_helper.fetch_expense_by_month()
    if monthly_data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense month wise from the database")
    return monthly_data
from Backend import db_helper

def test_fetch_expenses_for_date_15():
    abc = db_helper.fetch_expenses_for_date("2024-08-15")

    assert len(abc) == 1
    assert abc[0]['amount']==10.0
    assert abc[0]['category']=="Shopping"
    assert abc[0]['notes']=="Bought potatoes"

def test_fetch_expenses_for_date_15date():
    abc = db_helper.fetch_expenses_for_date("89868-08-15")
    assert len(abc) == 0

def test_fetch_expense_summary_invalid_range():
    summary=db_helper.fetch_expense_summary("2099-01-01","2099-12-01")
    assert len(summary) == 0


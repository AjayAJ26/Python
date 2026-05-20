import streamlit as st
from datetime import datetime
import requests

API_URL = "http://127.0.0.1:8000"

def add_update_tab():
    selected_date = st.date_input("Choose the Date", datetime(2024, 8, 1))
    response = requests.get(f"{API_URL}/expense/{selected_date}")
    if response.status_code == 200:
        existing_expense = response.json()
    else:
        st.error("Failed to retrieve expense")
        existing_expense = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # Reset session state only when the date changes
    if "last_date" not in st.session_state or st.session_state["last_date"] != selected_date:
        for i in range(5):
            if i < len(existing_expense):
                exp = existing_expense[i]
                st.session_state[f"amount_{i}"] = exp["amount"]
                st.session_state[f"category_{i}"] = exp["category"]
                st.session_state[f"notes_{i}"] = exp["notes"]
            else:
                st.session_state[f"amount_{i}"] = 0
                st.session_state[f"category_{i}"] = "Shopping"
                st.session_state[f"notes_{i}"] = ""
        st.session_state["last_date"] = selected_date

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        expenses = []
        for i in range(5):
            col1, col2, col3 = st.columns(3)

            with col1:
                amount_input = st.number_input(
                    label="Amount",
                    min_value=0,
                    step=1,
                    value=st.session_state[f"amount_{i}"],
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=categories.index(st.session_state[f"category_{i}"]),
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    label="",
                    value=st.session_state[f"notes_{i}"],
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        submit_button = st.form_submit_button("Submit")
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense["amount"] > 0]

            response = requests.post(f"{API_URL}/expense/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expense updated successfully")
                # Force refresh on next run so updated data is pulled
                st.session_state["last_date"] = None
            else:
                st.error("Failed to update expense")

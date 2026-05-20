import streamlit as st
from add_update_UI import add_update_tab
from analytics_category_UI import analytics_tab
from analytics_by_month_UI import analytics_months_tab

API_URL="http://127.0.0.1:8000"

st.title("Expense Management System")

tab1, tab2, tab3=st.tabs(["Add/Update","Analytics By Category","Analytics By Month"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()

with tab3:
    analytics_months_tab()
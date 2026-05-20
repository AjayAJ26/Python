import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL="http://127.0.0.1:8000"

def analytics_months_tab():
    response = requests.post(f"{API_URL}/analytics_by_month/")
    monthly_data = response.json()

    df=pd.DataFrame(monthly_data)
    df.rename(columns={
        "expense_months": "Month Number",
        "month_name": "Month Name",
        "total": "Total"
    },inplace=True)

    df_sorted=df.sort_values(by="Month Name",ascending=False)

    df_sorted.set_index("Month Number",inplace=True)

    st.title("Expense Breakdown By Months")
    st.bar_chart(data=df_sorted.set_index("Month Name")["Total"], use_container_width=True)

    df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)

    st.table(df_sorted.sort_index())

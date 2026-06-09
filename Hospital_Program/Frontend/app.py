import streamlit as st
from patient_details_UI import patient_details
from prescription_detail_UI import prescription_details


API_URL="http://127.0.0.1:8000"

st.title("Details Extraction")

tab1, tab2=st.tabs(["Patient Details","Prescription"])

with tab1:
    patient_details()

with tab2:
    prescription_details()


import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

def patient_details():

    st.header("Patient Details")
    if "patient_name" not in st.session_state:
        st.session_state["patient_name"] = ""
    if "mobile_number" not in st.session_state:
        st.session_state["mobile_number"] = ""
    if "hepatitis_b" not in st.session_state:
        st.session_state["hepatitis_b"] = ""
    if "medical_problems" not in st.session_state:
        st.session_state["medical_problems"] = ""
    if "dates" not in st.session_state:
        st.session_state["dates"] = datetime.today().date()
    uploaded_file = st.file_uploader(
        "Upload Patient Document",
        type=["pdf", "txt"],
        key="patient_uploader"
    )

    if uploaded_file is not None:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type
            )
        }

        data = {"file_format": "patient_details"}

        response = requests.post(
            f"{API_URL}/extract_from_doc",
            files=files,
            data=data
        )

        if response.status_code == 200:
            patient_data = response.json()
            st.session_state.patient_name = patient_data.get("patient_name", "")
            st.session_state.mobile_number = patient_data.get("mobile_number", "")
            st.session_state.hepatitis_b = patient_data.get("Hepatitis B", "")
            st.session_state.medical_problems = patient_data.get("Medical Problems", "")
            # st.write(patient_data)
        else:
            st.error(response.text)
            return
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        patient_id = st.text_input(
            "Patient ID",
            value=st.session_state.get("patient_id", ""),
            disabled=False
        )
        if st.button("Load Patient"):
            res = requests.get(
                f"{API_URL}/patient_details/{patient_id}",
            )
            if res.status_code == 200:
                data = res.json()

                if "error" not in data:
                    st.session_state.patient_name = data.get("patient_name", "")
                    st.session_state.mobile_number = data.get("mobile_number", "")
                    st.session_state.hepatitis_b = data.get("hepatitis_b", "")
                    st.session_state.medical_problems = data.get("medical_problems","")
                    st.session_state.dates = data.get("dates", datetime.today().date())
                    st.rerun()
                else:
                    st.error(data["error"])
    with col2:
        mobile_number = st.text_input(
            "Mobile Number",
            value=st.session_state.mobile_number
        )

    with col3:
        today_date = st.date_input(
            "Date",
            value=st.session_state.get(
                "dates",
                datetime.today().date()
            )
        )

    with col4:
        patient_name = st.text_input(
            "Patient Name",
            value=st.session_state.patient_name
        )

    hepatitis_b = st.text_input(
        "Hepatitis B Status",
        value=st.session_state.hepatitis_b
    )

    medical_problem = st.text_area(
        "Medical Problems",
        value=st.session_state.medical_problems
    )

    colA, colB,colC = st.columns(3)

    with colA:
        if st.button("Save Patient Details"):
            payload = {
                "id": patient_id,
                "patient_name": patient_name,
                "mobile_number": mobile_number,
                "hepatitis_b": hepatitis_b,
                "medical_problems": medical_problem,
                "today_date": str(today_date)
            }

            response = requests.post(
                f"{API_URL}/patient_details",
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                st.session_state["patient_id"] = result["patient_id"]
                st.success(f"Saved Successfully")
                st.rerun()
            else:
                st.error(response.text)

    with colB:
        if st.button("Update Patient Details"):
            payload = {
                "patient_name": patient_name,
                "mobile_number": mobile_number,
                "hepatitis_b": hepatitis_b,
                "medical_problems": medical_problem,
                "today_date": str(today_date)
            }

            res = requests.put(
                f"{API_URL}/patient_details/{patient_id}",
                json=payload
            )
            if res.status_code == 200:
                st.success("Patient  data updated successfully")
            else:
                st.error(res.text)

    with colC:
        if st.button("Delete Patient Details"):
            res = requests.delete(
                f"{API_URL}/patient_details/{patient_id}"
            )

            if res.status_code == 200:
                st.success("Patient deleted successfully")
            else:
                st.error(res.text)

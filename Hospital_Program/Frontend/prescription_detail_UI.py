from asyncio import timeout
from datetime import datetime
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def prescription_details():

    st.header("Prescription Details")
    st.session_state.setdefault("prescr_patient_name","")
    st.session_state.setdefault("prescr_patient_address","")
    st.session_state.setdefault("prescr_medicines","")
    st.session_state.setdefault("prescr_directions","")
    st.session_state.setdefault("prescr_refills","")
    st.session_state.setdefault("prescr_date",datetime.today().date())
    st.session_state.setdefault("prescr_id","")
    if "saved_parscr_id" in st.session_state:
        st.session_state["prescr_parscr_id"] = st.session_state.pop("saved_parscr_id")
    uploaded_file=st.file_uploader(
        "Upload Patient Document",
        type=["pdf","txt"],
        key="Prescription_uploader"
    )

    if uploaded_file is not None:
        files = {
            'file':(
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type
            )
        }

        data= {"file_format":"prescription"}

        response = requests.post(
            f"{API_URL}/extract_from_doc",
            files=files,
            data=data,
            timeout=60
        )

        if response.status_code==200:
            result = response.json()
            st.session_state["prescr_patient_name"] = result.get("patient_name","")
            st.session_state["prescr_patient_address"] = result.get("patient_address","")
            st.session_state["prescr_medicines"] = result.get("medicines","")
            st.session_state["prescr_directions"] = result.get("directions","")
            st.session_state["prescr_refills"] = result.get("refills","")
            st.session_state.setdefault("prescr_parscr_id","")
            # st.write(result)
        else:
            st.error(response.text)
            return

    col1, col2, col3,col4= st.columns(4)
    with col1:

        prescr_id = st.text_input(
            "Prescription ID",
            # value=st.session_state.get("prescr_id",""),
            key="prescr_parscr_id",
            disabled=False
        )
        if st.button("Load prescription",key="load_prescription"):
            res =requests.get(
                f"{API_URL}/prescription/{prescr_id}",
            )
            if res.status_code ==200:
                data=res.json()
                st.write(data)
                if "error" not in data:
                    st.session_state["prescr_patient_name"] = data.get("patient_name","")
                    st.session_state["prescr_patient_address"] = data.get("patient_address","")
                    st.session_state["prescr_medicines"] = data.get("medicines","")
                    st.session_state["prescr_directions"] = data.get("directions","")
                    st.session_state["prescr_refills"] =str(data.get("refills",""))
                    st.session_state["prescr_date"] = datetime.strptime(data.get("dates",str(datetime.today().date())),"%Y-%m-%d").date()
                    st.rerun()
                else:
                    st.error(data["error"])
    with (col2):
        st.text_input(
            "Patient Name",
            key="prescr_patient_name"
        )
    with (col3):
        if "prescr_refills" not in st.session_state or st.session_state["prescr_refills"]is None:
            st.session_state["prescr_refills"]=""
        else:
            st.session_state["prescr_refills"]=str(st.session_state["prescr_refills"])
        st.text_input(
            "Refills",
           key="prescr_refills"
    )

    with col4:
        row_date=st.session_state.get("prescr_date","None")
        if isinstance(row_date,str):
            try:
                st.session_state["prescr_date"]=datetime.strptime(row_date,"%Y-%m-%d").date()
            except:
                st.session_state["prescr_date"]=datetime.today().date()
        elif row_date is None:
            st.session_state["prescr_date"]=datetime.today().date()

        today_date = st.date_input(
            "Date",
            key="prescr_date"
            )
    st.text_area(
        "Address",
        key="prescr_patient_address",
        height=80
    )
    st.text_area(
        "Medicines",
        key="prescr_medicines",
        height=200
    )
    st.text_area(
        "Directions",
        key="prescr_directions",
        height=150
    )

    colA,colB,colC = st.columns(3)

    with colA:
        if st.button("Save precsciption Data",key="save_prescription"):
            payload = {
                "prescr_id":prescr_id,
                "patient_name":st.session_state["prescr_patient_name"],
                "patient_address":st.session_state["prescr_patient_address"],
                "medicines":st.session_state["prescr_medicines"],
                "directions":st.session_state["prescr_directions"],
                "refills":st.session_state["prescr_refills"],
                "today_date":str(today_date)
            }
            response = requests.post(
                f"{API_URL}/prescription",
                json=payload
            )

            if response.status_code==200:
                result = response.json()
                st.session_state["saved_parscr_id"]=str(result.get("prescr_id",""))
                st.success("Saved successfully")
                st.rerun()
            else:
                st.error(response.text)

    with colB:
        if st.button("Update Prescription Details",key="update_prescription"):
            payload={
                "patient_name":st.session_state["prescr_patient_name"],
                "patient_address":st.session_state["prescr_patient_address"],
                "medicines":st.session_state["prescr_medicines"],
                "directions":st.session_state["prescr_directions"],
                "refills":st.session_state["prescr_refills"],
                "today_date":str(today_date)
            }
            res = requests.put(
                f"{API_URL}/prescription/{prescr_id}",
                json=payload
            )
            if res.status_code==200:
                st.success("Prescription Updated successfully")
            else:
                st.error(res.text)
    with colC:
        if st.button("Delete prescription Details",key="delete_prescription"):
            res = requests.delete(
                f"{API_URL}/prescription/{prescr_id}",
            )
            if res.status_code==200:
                st.success("Prescription Deleted successfully")
            else:
                st.error(res.text)
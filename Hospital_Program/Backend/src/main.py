from fastapi import FastAPI, File, UploadFile, Form,HTTPException
import uvicorn
import os
import uuid
import db_helper
from parser_prescription import PrescriptionParser
from extractor import extract
from pydantic import BaseModel
from datetime import date

class PatientDetails(BaseModel):
    patient_name:str
    mobile_number:str
    hepatitis_b:str
    medical_problems:str
    today_date:date

class PatientDelete(BaseModel):
    id: int

class Prescription(BaseModel):
    patient_name: str
    patient_address: str
    medicines: str
    directions: str
    refills: str
    today_date: date


app = FastAPI()


@app.post("/extract_from_doc")
def extract_from_doc(
    file_format: str = Form(...),   # form field
    file: UploadFile = File(...),   # file upload
):

    # Read file contents
    contents = file.file.read()
    file_path="../uploads/" +str(uuid.uuid4())+".pdf"
    with open(file_path, "wb") as f:
        f.write(contents)

    try:
         data = extract(file_path,file_format)
    except Exception as e:
        data = {
            'error':str(e)
        }

    if os.path.exists(file_path):
        os.remove(file_path)
    return data

@app.post("/patient_details")
def save_or_update_data(patient_data: dict):
    patient_id=db_helper.insert_patient_details(
        patient_data["patient_name"],
        patient_data["mobile_number"],
        patient_data["hepatitis_b"],
        patient_data["medical_problems"],
        patient_data["today_date"]
    )

    return {
        "message":"patient data saved successfully",
        "patient_id":patient_id
    }

@app.put("/patient_details/{patient_id}")
def update_patient( patient_id:int ,patient:PatientDetails):
    try:
       rows=db_helper.update_patient_details(
           patient_id,
           patient.patient_name,
           patient.mobile_number,
           patient.hepatitis_b,
           patient.medical_problems,
           patient.today_date
       )

       return {"message":"patient updated successfully",
        "rows_updated":rows
        }
    except Exception as e:
        print("Update ERROR:",e)
        raise


@app.delete("/patient_details/{patient_id}")
def delete_patient(patient_id:int):
    try:
        rows=db_helper.delete_patient_details(patient_id)
        if rows==0:
            return {"error":"Patient not found"}

        return {"message":"patient deleted successfully"}
    except Exception as e:
        return {"error":str(e)}


@app.get("/patient_details/{patient_id}")
def get_patient_details(patient_id:int):
    patient=db_helper.get_patient_by_id(patient_id)
    if patient:
        return patient

    return {"error":"patient not found"}

@app.post("/prescription")
def save_prescription_data(prescription:Prescription):
    prescr_id=db_helper.insert_prescription_details(
        prescription.patient_name,
        prescription.patient_address,
        prescription.medicines,
        prescription.directions,
        prescription.refills,
        prescription.today_date
    )
    return {
        "message":"prescription data saved successfully",
        "prescr_id":prescr_id
    }

@app.put("/prescription/{prescr_id}")
def update_prescription(prescr_id:int, prescription:Prescription):
    try:
        rows=db_helper.update_prescription_details(
            prescr_id,
            prescription.patient_name,
            prescription.patient_address,
            prescription.medicines,
            prescription.directions,
            prescription.refills,
            prescription.today_date
        )
        return {"message":"prescription updated successfully",
                "rows_updated":rows}
    except Exception as e:
        print("Update ERROR:",e)
        raise

@app.delete("/prescription/{prescr_id}")
def delete_prescription(prescr_id:int):
    try:
        rows=db_helper.delete_prescription_details(prescr_id)
        if rows==0:
            return {"error":"Prescription not found"}

        return {"error":"prescription deleted successfully"}
    except Exception as e:
        return {"error":str(e)}

@app.get("/prescription/{prescr_id}")
def get_prescription(prescr_id:int):
    prescription=db_helper.get_prescription_by_id(prescr_id)
    if prescription:
        return prescription
    return {"error":"prescription not found"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

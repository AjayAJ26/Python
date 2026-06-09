import mysql.connector
from contextlib import contextmanager
from pygments.lexers import data


@contextmanager
def get_db_cursor(commit=False):
    connection= mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="hospital_db"
    )
    if connection.is_connected():
        print("Connection is successful")
    else:
        print("Connection Error")

    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception as e:
        print("BD Error:",e)
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

def insert_patient_details(patient_name,mobile_number,hepatitis_b,medical_problems,today_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """INSERT INTO patients
            (   
                patient_name,
                mobile_number,
                hepatitis_b,
                medical_problems,
                dates
            )
            VALUES (%s, %s, %s, %s,%s)""",
            (
                patient_name,
                mobile_number,
                hepatitis_b,
                medical_problems,
                today_date
            )
        )
        return cursor.lastrowid

def update_patient_details(patient_id,patient_name,mobile_number,hepatitis_b,medical_problems,today_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """UPDATE patients 
            SET 
            patient_name=%s,
            mobile_number=%s,
            hepatitis_b=%s,
            medical_problems=%s,
            dates=%s
            WHERE id=%s""",
            (
                patient_name,
                mobile_number,
                hepatitis_b,
                medical_problems,
                today_date,
                patient_id
                )
        )
        rows=cursor.rowcount
        print("rows:",rows)
    return rows


def delete_patient_details(patient_id):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """DELETE FROM patients 
            where id =%s
            """,
            (patient_id,)
        )
        print("Rows Deleted",cursor.rowcount)
        return cursor.rowcount

def get_patient_by_id(patient_id):
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM patients WHERE id = %s",
            (patient_id,)
        )
        return cursor.fetchone()

def insert_prescription_details(patient_name,patient_address,medicines,directions,refills,today_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """INSERT INTO prescriptions (
            patient_name,
            patient_address,
            medicines,
            directions,
            refills,
            dates
        )
        VALUES(%s,%s,%s,%s,%s,%s)""",
            (
                patient_name,
                patient_address,
                medicines,
                directions,
                refills,
                today_date
            )
        )
        return cursor.lastrowid

def update_prescription_details(prescr_id,patient_name,patient_address,medicines,directions,refills,today_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """UPDATE prescriptions 
            SET 
            patient_name=%s,
            patient_address=%s,
            medicines=%s,
            directions=%s,
            refills=%s,
            dates=%s
            WHERE pre_id=%s""",
            (
                patient_name,
                patient_address,
                medicines,
                directions,
                refills,
                today_date,
                prescr_id
            )
        )
        rows=cursor.rowcount
        print("rows:",rows)
    return rows
def delete_prescription_details(prescr_id):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """DELETE FROM prescriptions 
            WHERE pre_id=%s""",
            (prescr_id,)
        )
        print("Rows Deleted",cursor.rowcount)
        return cursor.rowcount
def get_prescription_by_id(prescr_id):
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM prescriptions WHERE pre_id = %s",
            (prescr_id,)
        )
        return cursor.fetchone()
from Backend.src.parser_patient import PatientParser
import pytest

@pytest.fixture
def doc_1_kathy():
    document_text = '''17/12/2020

Patient Medical Record

Patient Information Birth Date
Kathy Crawford May 6 1972
(737) 988-0851 Weight’
9264 Ash Dr 95
New York City, 10005 .
United States Height:
190
In Casc of Emergency
7 ee
Simeone Crawford 9266 Ash Dr
New York City, New York, 10005
Home phone United States
(990) 375-4621
Work phone

Genera! Medical History

a

a

a ea A CE i a

Chicken Pox (Varicella): Measies:

IMMUNE IMMUNE

Have you had the Hepatitis B vaccination?
No

List any Medical Problems (asthma, seizures, headaches):

Migraine

CO
aa'''
    return PatientParser(document_text)

def test_patient_name(doc_1_kathy):
    assert doc_1_kathy.get_patient_name() == 'Kathy Crawford'

def test_mobile_number(doc_1_kathy):
    assert doc_1_kathy.get_field("mobile_number") == '(737) 988-0851'

def test_hepatitis_b(doc_1_kathy):
    assert doc_1_kathy.get_field("Hepatitis B") == 'No'

def test_medical_problems(doc_1_kathy):
    assert doc_1_kathy.get_field("Medical Problems") == 'Migraine'
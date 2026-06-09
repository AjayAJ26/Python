from Backend.src.parser_prescription import PrescriptionParser
import pytest

@pytest.fixture
def doc_1_maria():
    document_text = '''Dr John Smith, M.D
    2 Non-Important Street,
    New York, Phone (000)-111-2222

    Name: Marta Wyan Date: 5/11/2022

    Address: 9 tennis court, new Russia, DC

    Prednisone 20 mg
    Lialda 2.4 gram

    Directions:
    Prednisone, Taper 5 mg every 3 days,

    Finish in 2.5 weeks
    Lialda - take 2 pill everyday for 1 month

    Refill: 2. times'''
    return PrescriptionParser(document_text)


@pytest.fixture
def doc_3_empty():
     return PrescriptionParser('')

@pytest.fixture
def doc_1_ajay():
    document_text = '''Dr John Smith, M.D
    2 Non-Important Street,
    New York, Phone (000)-111-2222

    Name: Ajay Jadhav Date: 5/11/2022

    Address: 9 tennis court, new Russia, DC

    Prednisone 20 mg
    Lialda 2.4 gram

    Directions:
    Prednisone, Taper 5 mg every 3 days,

    Finish in 2.5 weeks
    Lialda - take 2 pill everyday for 1 month

    Refill: 2. times'''
    return PrescriptionParser(document_text)

def test_get_name(doc_1_maria, doc_1_ajay, doc_3_empty):
    assert doc_1_maria.get_field("patient_name")=="Marta Wyan"
    assert doc_1_ajay.get_field("patient_name") == "Ajay Jadhav"
    assert doc_3_empty.get_field("patient_name") == None


def test_get_address(doc_1_maria,doc_1_ajay):
     assert doc_1_maria.get_field("patient_address")=="9 tennis court, new Russia, DC"
     assert doc_1_ajay.get_field("patient_address") == "9 tennis court, new Russia, DC"

def test_get_medicines(doc_1_maria,doc_1_ajay,doc_3_empty):
    assert doc_1_maria.get_field("medicines")=='''Prednisone 20 mg
    Lialda 2.4 gram'''
    assert doc_1_ajay.get_field("medicines")=='''Prednisone 20 mg
    Lialda 2.4 gram'''
    assert doc_3_empty.get_field("medicines")==None


def test_get_directions(doc_1_maria,doc_1_ajay,doc_3_empty):
    assert doc_1_maria.get_field("directions")=='''Prednisone, Taper 5 mg every 3 days,

    Finish in 2.5 weeks
    Lialda - take 2 pill everyday for 1 month'''
    assert doc_1_maria.get_field("directions")=='''Prednisone, Taper 5 mg every 3 days,

    Finish in 2.5 weeks
    Lialda - take 2 pill everyday for 1 month'''
    assert doc_3_empty.get_field("directions")==None

def test_get_refills(doc_1_maria,doc_1_ajay,doc_3_empty):
    assert doc_1_maria.get_field("refills")=='2'
    assert doc_1_ajay.get_field("refills")=='2'
    assert doc_3_empty.get_field("refills")==None

def test_parse(doc_1_maria,doc_1_ajay,doc_3_empty):
    record_maria= doc_1_maria.parse()
    assert record_maria['patient_name'] == 'Marta Wyan'
    assert record_maria['patient_address'] == '9 tennis court, new Russia, DC'
    assert record_maria['medicines'] == '''Prednisone 20 mg
    Lialda 2.4 gram'''
    assert record_maria['directions'] == '''Prednisone, Taper 5 mg every 3 days,

    Finish in 2.5 weeks
    Lialda - take 2 pill everyday for 1 month'''

    assert record_maria['refills'] == '2'

    record_ajay= doc_1_ajay.parse()
    assert record_ajay=={
        'patient_name':'Ajay Jadhav',
        'patient_address':'9 tennis court, new Russia, DC',
        'medicines':'''Prednisone 20 mg
    Lialda 2.4 gram''',
        'directions':'''Prednisone, Taper 5 mg every 3 days,

    Finish in 2.5 weeks
    Lialda - take 2 pill everyday for 1 month''',
        'refills':'2'
    }

    record_empty = doc_3_empty.parse()
    assert record_empty == {
        'patient_name': None,
        'patient_address': None,
        'medicines': None,
        'directions': None,
        'refills': None
    }



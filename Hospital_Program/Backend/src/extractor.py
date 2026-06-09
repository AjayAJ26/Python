from pdf2image import convert_from_path
import pytesseract
import util
from util import preprocess_image
from parser_prescription import PrescriptionParser
from parser_patient import PatientParser

POPPLER_PATH= r"C:\poppler-26.02.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract(file_path,file_format):
    pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
    document_text=''
    if len(pages)>0:
        page = pages[0]
        processed_image=util.preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang="eng")
        document_text = '\n'+text

    if file_format == 'prescription':
       extracted_data=PrescriptionParser(document_text).parse()
    elif file_format == 'patient_details':
        extracted_data=PatientParser(document_text).parse()

    return extracted_data

if __name__ == '__main__':
    data = extract('../docs/patient_details/pd_1.pdf','patient_details')
    print(data)
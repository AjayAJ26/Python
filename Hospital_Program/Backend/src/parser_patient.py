import re

from parser_generic import MedicalDocParser


class PatientParser(MedicalDocParser):
    def __init__(self,text):
        MedicalDocParser.__init__(self,text)

    def parse(self):
        return {
            'patient_name':self.get_patient_name(),
            'mobile_number':self.get_field('mobile_number'),
            'Hepatitis B':self.get_field('Hepatitis B'),
            'Medical Problems':self.get_field('Medical Problems')
        }


    def get_field(self,filed_name):
        pattern_dict={
            # 'patient_name':{'pattern':'Date(.*) May','flags':re.DOTALL},
            'mobile_number':{'pattern':r'Date\(\d{3}\)-\d{3}-\d{4}|\(\d{3}\)\s\d{3}-\d{4}|\d{10}Weight','flags':re.DOTALL},
            'Hepatitis B':{'pattern':r'Have you had the Hepatitis B vaccination\?(.*)List','flags':re.DOTALL},
            'Medical Problems':{'pattern':r'Medical Problems \(asthma, seizures, headaches\):([^\r]*)\s(?:)','flags':re.DOTALL}
        }
        pattern_object=pattern_dict.get(filed_name)
        if pattern_object:
            match=re.findall(pattern_object['pattern'],self.text,flags=pattern_object['flags'])
            if len(match)>0:
                return match[0].strip()

    def remove_noice(self, name):
        # Remove the word 'Date' if present
        name = name.replace('Date', '').strip()
        # Regex to match month + day + year
        date_pattern = r'(?:Jan|Feb|March|April|May|June|July|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{4}'
        date_match = re.search(date_pattern, name)
        if date_match:
            # Remove the entire date string
            name = name.replace(date_match.group(), '').strip()
        return name

    def get_patient_name(self):
        pattern = r'Patient Information Birth Date\s+(.+?)\s+(?:Jan|Feb|March|April|May|June|July|Aug|Sep|Oct|Nov|Dec)'
        match = re.search(pattern, self.text, flags=re.DOTALL)
        name = ''
        if match:
            name = match.group(1).strip()
        return name


if __name__=='__main__':
    document_text='''17/12/2020

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

List any Medical Problems (asthma, seizures, headaches}:

Migraine

CO
aa

'''
    pp = PatientParser(document_text)
    print(pp.parse())
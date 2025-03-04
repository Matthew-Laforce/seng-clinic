#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'patient.py':

This file is re-used from assignment 4 with minimal alterations. The Patient 
method is a constructor of an object that represents a patient within this 
framework. Patients are stored inside 'PatientDAOJSON' instances, and they 
contain a 'PatientRecord' to store notes. 

============================================================================ """

# IMPORTS:
from clinic.patient_record import PatientRecord

class Patient:
    def __init__(self, phn, name, birth_date, phone, email, address, autosave = False):
        # Initialize the given values
        self.phn = int(phn)
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.autosave = autosave        
        # Assign the patient a patient_record
        self.record = PatientRecord(self.phn, self.autosave)
        
    def __str__(self):
        return f"\nPHN: {self.phn} \nName: {self.name} \nBirthdate: {self.birth_date} \nPhone: {self.phone} \nEmail: {self.email} \nAddress: {self.address}"
        
    # Considers two patients equal if all non-autosave values match    
    def __eq__(self, other):
        try:
            if (self.phn == other.phn and self.name == other.name and \
                self.birth_date == other.birth_date and self.phone == \
                other.phone and self.email == other.email and \
                self.address == other.address):
                return True
            else:
                return False
        except:
            return False

    def get_phn(self):
        return self.phn
    
    def get_name(self):
        return self.name
    
    def get_birthdate(self):
        return self.birth_date
    
    def get_phone(self):
        return self.phone
    
    def get_email(self):
        return self.email
    
    def get_address(self):
        return self.address

    def change_patient(self, phn, name, birth_date, phone, email, address): 
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address

# ==============================================================================

def main():
    print("Main file called as 'patient.py'")

if __name__ == "__main__":
    main()

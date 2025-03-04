#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'patient_encoder.py':

This file is re-used from assignment 4 with minimal alterations. For the sake 
of persistence, JSON files are used to store 'Patient' objects. This file is an 
encoder which translates patients into something JSON storable.

** Originally repurposed from the Lab 9 encoder file **

============================================================================ """

# IMPORTS:
from clinic.patient import Patient
from json import JSONEncoder

# Closely follows the formatting of the Lab 9 product encoder
class PatientEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Patient):
            return {"__type__": "Patient", "phn": int(obj.phn), "name": \
                    obj.name, "birth_date": obj.birth_date, "phone": \
                    obj.phone, "email": obj.email, "address": obj.address, \
                    "autosave": obj.autosave}
        return super().default(obj)

# ==============================================================================

def main():
    print("Main file called as 'patient_encoder.py'")

if __name__ == "__main__":
    main()

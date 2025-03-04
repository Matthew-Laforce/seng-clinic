#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'patient_decoder.py':

This file is re-used from assignment 4 with minimal alterations. For the sake 
of persistence, JSON files are used to store 'Patient' objects. This file is a 
decoder which translates JSON files back into patients.

** Originally repurposed from the Lab 9 decoder file **

============================================================================ """

# IMPORTS:
from clinic.patient import Patient
from json import JSONDecoder

# Closely follows the formatting of the Lab 9 product decoder
class PatientDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
        
    def object_hook(self, dct):
        if '__type__' in dct and dct['__type__'] == 'Patient':
            return Patient(dct['phn'], dct['name'], dct['birth_date'],\
                           dct['phone'], dct['email'], dct['address'],\
                           dct['autosave'])
        return dct

# ==============================================================================

def main():
    print("Main file called as 'patient_decoder.py'")

if __name__ == "__main__":
    main()

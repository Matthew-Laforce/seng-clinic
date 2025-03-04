#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'patient_dao_json.py':

This file is reused from assignment 4 with minimal alterations. It's main 
purpose is to store and manipulate a collection of patient objects. When a 
patient is created, they are stored in a 'PatientDAOJSON' which resides in 
'Controller'.

For the sake of simplicity, the class saves note information after each update.
This would not be optimal for a large, performance-intense system, but it
works great here.

============================================================================ """

# EXCEPTIONS:
from clinic.exception.illegal_operation_exception import IllegalOperationException

# IMPORTS:
import json
from clinic.patient import Patient
from clinic.dao.patient_dao import *
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder

class PatientDAOJSON:
    def __init__(self, autosave = False):
        # Standard initialization of PatientDAOJSON
        self.autosave = autosave
        self.patient_data = {}
        # When persistence is enabled, load patient data from a JSON
        if self.autosave is True:
            self.load_patients()
            
    def __str__(self):
        return f"Autosave: {self.autosave}, Patient Data: {self.patient_data}"
    
    # Considers autosave and patient_data in comparing 'PatientDAOJSON's
    def __eq__(self, other):
        try:
            if self.autosave == other.autosave and\
               self.patient_data == other.patient_data:
                return True
            else:
                return False
        except:
            return False
        
    # Helper method- when persistence is enabled, saves patient data as a JSON
    def save_patients(self):
        if self.autosave is True:
            with open("clinic/patients.json", "w") as raw_json:
                json.dump(self.patient_data, raw_json, cls=PatientEncoder)
    
    # Helper method- if a JSON exists, convert it into a patient dictionary    
    def load_patients(self):
        try:
            with open("clinic/patients.json", "r") as raw_json:
                # Decode the JSON file into a dictionary
                raw_patients = json.load(raw_json, object_hook=\
                                         PatientDecoder().object_hook)
                # Convert each PHN back into an integer
                for phn, patient in raw_patients.items():
                    int_phn = int(phn)
                    self.patient_data[int_phn] = patient
        # If no JSON exists, use the pre-made empty dictionary
        except (FileNotFoundError):
            pass
    
    # Returns a patient if their PHN exists in 'patient_data'
    def search_patient(self, phn):
        return self.patient_data.get(phn, None)
    
    def create_patient(self, phn, name, birth_date, phone, email, address):
        """
        Accepts PHN, an integer, and a series of strings as input. Outputs
        either None, if no patient is created, else outputs that patient.
        Requires a logged in user and a unique PHN.
        """
        # Reject creation if the PHN is not free to use
        if self.patient_data.get(phn, None) is not None:
            raise IllegalOperationException("Error: PHN already in use")
        # Otherwise, create the patient, append them to 'patient_data'
        else:
            self.patient_data[phn] = Patient(phn, name, birth_date, phone, \
                                             email, address, self.autosave)
            # Update the patient JSON to reflect the addition
            self.save_patients()
            return self.patient_data[phn]

    def retrieve_patients(self, name):
        """
        Accepts 'name', a string, as input. Returns a list of any and all
        stored patients whose name matches the search string. If no patients
        match, returns an empty list.
        """
        patient_match = []
        for entry in self.patient_data.values():
            patient = entry.get_name()
            # Matches cause 'find' to return a positive integer: append
            if patient.find(name) != (-1):
                patient_match.append(entry)     
        return patient_match
    
    def update_patient(self, old_phn, phn, name, birth_date, phone, email, address):
        """
        Accepts two PHNs and several patient information strings as input.
        Outputs True if patient creation succeeds, else raises an error. A
        successful update requires a unique PHN and an existant patient.
        """
        # Ensure any PHN changes do not cause conflicts
        if phn != old_phn and self.patient_data.get(phn, None) is not None:
            raise IllegalOperationException("Error: in-use PHN")
        # Confirm the existance of the original patient
        elif self.patient_data.get(old_phn, None) is None:
            raise IllegalOperationException("Error: patient not in the record")
        # After those checks update the patient
        else:
            # Find, change, delete, then replace the patient
            patient = self.search_patient(old_phn)
            patient.change_patient(phn, name, birth_date, phone, email, address)
            del self.patient_data[old_phn]            
            self.patient_data[phn] = patient
            # Update the patient JSON to reflect the changes
            self.save_patients()
            return True
    
    def delete_patient(self, phn):
        """
        Accepts phn, a patient identifier, as input. Returns an exception if 
        the patient does not exist, otherwise, deletes the patient and returns 
        True.
        """
        # Confirm the existance of the patient
        if self.search_patient(phn) is None:
            raise IllegalOperationException("Error: patient does not exist")
        else:
            del self.patient_data[phn]
            # Update the patient JSON to reflect the removal
            self.save_patients()
            return True
    
    def list_patients(self):
        """
        Returns a list of all Patient objects that exist inside patient_data.
        If there are no patients, returns an empty list.
        """
        patient_list =  []
        for patient in self.patient_data:
            patient_list.append(self.patient_data[patient])
        return patient_list

# ==============================================================================

def main():
    print("Main file called as 'patient_dao_json.py'")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'controller.py':

This is the main file for Assignment 4, and is reused here with minimal 
alterations. All of the user stories are called from here. Moreover, 
Controller handles the user login logic, as well as tracking the currently 
selected patient (if one exists). 

Controller contains a PatientDAOJSON, which in turn contains patient objects.

Note that the method 'get_password_hash' is borrowed from Lab 9.

============================================================================ """

# EXCEPTIONS:
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

# IMPORTS:
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.patient import Patient
import unittest
import hashlib

class Controller:
    def __init__(self, autosave = False):
        # Standard controller initialization
        self.autosave = autosave
        self.logged_in = False
        self.current_patient = None
        self.patient_dao = PatientDAOJSON(self.autosave)
        # Persistence handling for controller
        if self.autosave is False:
            # Placeholder users hardcoded in for testing
            self.users = {"user" : "123456", "ali" : "@G00dPassw0rd"}
        else:
            # Dynamically load user information
            self.users = self.load_users()
        
    # Prints controller information as a string
    def __str__(self):
        return f"autosave: {self.autosave}, logged_in: {self.logged_in}, current_patient: {self.current_patient}, users: {self.users}"
    
    # Considers Controller objects equal if their four traits all match
    def __eq__(self, other):
        try:
            if self.autosave == other.autosave and \
               self.logged_in == other.logged_in and \
               self.current_patient == other.current_patient and\
               self.users == other.users:
                return True
            else:
                return False
        except:
            return False

    # Confirm whether or not the controller is logged in
    def is_logged(self):
        if self.logged_in is False:
            raise IllegalAccessException("Error: not logged in")
        
    # Confirm whether an operation tries to modify the current patient
    def is_current_patient(self, phn):
        if self.current_patient is self.search_patient(phn):
            raise IllegalOperationException("Error: cannot update 'current_patient'")
        
    # Confirm the existance of the current patient
    def check_current_exists(self):
        if self.current_patient is None:
            raise NoCurrentPatientException("Error: no patient selected")
        
    # Generates a list of all registered users (when autosave is True)
    def load_users(self):
        users = {}
        with open("clinic/users.txt", "r") as file_text:
            for line in file_text:
                # Strip any whitespace out of the line, split into a list
                line = line.strip()
                user = line.split(",")
                # Append user's name (index 0) and password hash (index 1)
                users[user[0]] = user[1]
        return users
    
    # Decodes a user password: ** Borrowed from Lab 9 **
    def get_password_hash(self, password):
        encoded_password = password.encode('utf-8')     # Convert the password to bytes
        hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
        hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
        return hex_dig    
    
# ==============================================================================       
    
    # USER STORY 1
    def login(self, username, password):
        """
        Accepts 'username' and 'password' strings as input. Outputs True if
        the login information matches hardcoded values, else outputs False.
        
        Sets login status for 'controller'.
        """
        # Reject login if already logged in
        if self.logged_in == True:
            raise DuplicateLoginException("Error: already logged in.")
        # Verify the existance of the username
        elif self.users.get(username):
            # Get the stored password of 'username', compare to 'password'
            stored_password = self.users.get(username)
            # If autosave is True, then hash 'password' before comparison
            if self.autosave == True:
                password = self.get_password_hash(password)
            # Confirm the validity of the login attempt
            if password == stored_password:
                print("Logging in.")
                self.logged_in = True
                return True
        # Reject invalid user logins
        raise InvalidLoginException("Error: invalid login information.") 
    
    # USER STORY 2
    def logout(self):
        """
        No input required. Outputs True if the user was logged in, then logs
        them out. Else, outputs False.
        """
        # Reject logout request from a logged out user
        if not self.logged_in == True:
            raise InvalidLogoutException("Error: not logged in, cannot log out")
        # Otherwise, log the user out
        print("Logging out.")
        self.unset_current_patient()
        self.logged_in = False
        return True
    
    # USER STORY 3
    def search_patient(self, phn):
        self.is_logged()
        if int(phn) != phn:
            raise IllegalOperationException("Error: PHNs must be integers")        
        return self.patient_dao.search_patient(phn)

    # USER STORY 4
    def create_patient(self, phn, name, birth_date, phone, email, address):
        self.is_logged()
        if int(phn) != phn:
            raise IllegalOperationException("Error: PHNs must be integers")        
        return self.patient_dao.create_patient(phn, name, birth_date, phone,\
                                               email, address)
    
    # USER STORY 5
    def retrieve_patients(self, name):
        self.is_logged()
        return self.patient_dao.retrieve_patients(name)
    
    # USER STORY 6
    def update_patient(self, old_phn, phn, name, birth_date, phone, email,\
                       address):
        self.is_logged()
        if int(phn) != phn or int(old_phn) != old_phn:
            raise IllegalOperationException("Error: PHNs must be integers")        
        self.is_current_patient(old_phn)
        return self.patient_dao.update_patient(old_phn, phn, name, birth_date,\
                                               phone, email, address)

    # USER STORY 7
    def delete_patient(self, phn):
        self.is_logged()
        self.is_current_patient(phn)
        return self.patient_dao.delete_patient(phn)

    # USER STORY 8
    def list_patients(self):
        self.is_logged()
        return self.patient_dao.list_patients()
    
    def get_current_patient(self):
        self.is_logged()
        return self.current_patient
    
    # USER STORY 9
    def set_current_patient(self, phn):
        self.is_logged()
        if int(phn) != phn:
            raise IllegalOperationException("Error: PHNs must be integers")        
        if self.patient_dao.patient_data.get(phn, None) is None:
            raise IllegalOperationException("Error: specified patient does not exist")
        else:
            self.current_patient = self.patient_dao.search_patient(phn)
            return self.current_patient
    
    def unset_current_patient(self):
        self.is_logged()
        self.current_patient = None
        return True
    
    # USER STORY 10
    def create_note(self, text):
        self.is_logged()
        self.check_current_exists()
        return self.current_patient.record.create_note(text)

    # USER STORY 11
    def retrieve_notes(self, text):
        self.is_logged()
        self.check_current_exists()
        return self.current_patient.record.retrieve_notes(text)
    
    def search_note(self, note_index):
        self.is_logged()
        self.check_current_exists()
        if int(note_index) != note_index:
            raise IllegalOperationException("Error: note indexes must be integers")          
        return self.current_patient.record.search_note(note_index)
        
    # USER STORY 12
    def update_note(self, note_index, text):
        self.is_logged()
        self.check_current_exists()
        if int(note_index) != note_index:
            raise IllegalOperationException("Error: note indexes must be integers")        
        return self.current_patient.record.update_note(note_index, text)
    
    # USER STORY 13
    def delete_note(self, note_index):
        self.is_logged()
        self.check_current_exists()
        if int(note_index) != note_index:
            raise IllegalOperationException("Error: note indexes must be integers")        
        patient = self.get_current_patient()
        return self.current_patient.record.delete_note(note_index)
    
    # USER STORY 14
    def list_notes(self):
        self.is_logged()
        self.check_current_exists()
        patient = self.get_current_patient()
        return self.current_patient.record.list_notes()    

# ==============================================================================

def main():
    print("Main file called as 'controller.py'")

if __name__ == "__main__":
    main()

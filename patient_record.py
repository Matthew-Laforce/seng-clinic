#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'patient_record.py':

This file is re-used from assignment 4 with minimal alterations. 'PatientRecord' 
acts as an intermediate between 'Patient' objects and the method 
'NoteDAOPickle'. In assignment 3, this method was very important, though at 
this point it does almost nothing - for the sake of the assignment this file 
must be included. 

If Patients had other data collections rather than just 'Note' objects
(which are stored in NoteDAOPickle), this is where they would go I suppose. 

============================================================================ """

# IMPORTS:
from clinic.dao.note_dao_pickle import NoteDAOPickle
from clinic.note import Note

class PatientRecord:
    def __init__(self, phn, autosave = False):        
        # Basically this just passes parameters to NoteDAOPickle
        self.phn = phn
        self.autosave = autosave
        self.note_dao_pickle = NoteDAOPickle(self.phn, self.autosave)
        
    def __str__(self):
        return f"note_dao_pickle: {self.note_dao_pickle}"
    
    # Considers two PatientRecords equal if their three traits match
    def __eq__(self, other):
        try:
            if self.phn == other.phn and self.note_dao_pickle == \
               other.note_dao_pickle and self.autosave == other.autosave:
                return True
            else:
                return False
        except:
            return False
        
    def create_note(self, text):
        return self.note_dao_pickle.create_note(text)
        
    def retrieve_notes(self, text):
        return self.note_dao_pickle.retrieve_notes(text)
        
    def search_note(self, note_index):
        return self.note_dao_pickle.search_note(note_index)
     
    def update_note(self, note_index, text):
        return self.note_dao_pickle.update_note(note_index, text)
    
    def delete_note(self, note_index):
        return self.note_dao_pickle.delete_note(note_index)
    
    def list_notes(self):
        return self.note_dao_pickle.list_notes()
     
# ==============================================================================

def main():
    print("Main file called as 'patient_record.py'")

if __name__ == "__main__":
    main()

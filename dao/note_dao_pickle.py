#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'note_dao_pickle.py':

This file is re-used from assignment 4 with minimal alterations. The file's 
main purpose is to store and manipulate a collection of note objects. That is, 
each 'Patient' object has a 'PatientRecord', and each record contains a 
'NoteDAOPickle' to contain notes. 

For the sake of simplicity, the class saves note information after each update. 
This would not be optimal for a large, performance-intense system, but it
works great here.

============================================================================ """

# IMPORTS:
from clinic.dao.note_dao import *
from clinic.note import Note
import hashlib
import pickle

class NoteDAOPickle:
    def __init__(self, phn, autosave = False):
        # Standard intialization of NoteDAOPickle
        self.filename = "clinic/records/" + str(phn) + ".dat"
        self.autosave = autosave
        self.autocounter = 0        # Represents current note count
        self.position = 0           # Counts total notes created
        self.notes = {}
        # When persistence is enabled, load patient note file
        if self.autosave is True:
            self.load_notes()
            
    def __str__(self):
        return f"Autosave: {self.autosave}, Autocounter: {self.autocounter}, Position: {self.position}, Notes: {self.notes}"
    
    # Considers two PatientRecords equal if their four traits match
    def __eq__(self, other):
        try:
            if self.notes == other.notes and self.autocounter == \
               other.autocounter and self.position == other.position and\
               self.notes == other.notes:
                return True
            else:
                return False
        except:
            return False
        
    # Helper method: when persistence is enabled, saves the note dictionary   
    def save_notes(self):
        if self.autosave is True:
            with open(self.filename, "wb") as raw_notes:
                pickle.dump(self.notes, raw_notes)
        
    # Helper method: if some 'this_phn.dat' exists, unpickle it
    def load_notes(self):
        try:
            with open(self.filename, "rb") as pickled_notes:
                self.notes = pickle.load(pickled_notes)
            # Set 'autocounter' and 'position' using the dictionary
            self.autocounter = len(self.notes)          # Note count
            self.position = next(reversed(self.notes))  # Final key
        # If no .dat exists, use the pre-set values
        except:
            pass
    
    def create_note(self, text):
        """
        Accepts a text string as input. This text is used to create a Note
        object, which is then appended to the 'notes' dictionary. Returns
        the resulting note.
        """
        # Increment the note counters
        self.autocounter += 1
        self.position += 1           
        # Create the note, save it if persistence is enabled, return it
        self.notes[self.position] = Note(self.position, text)
        self.save_notes()     
        return self.notes[self.position]
    
    def retrieve_notes(self, text):
        """
        Accepts 'text', a string to search the existing notes for, as input. 
        Returns an empty list if no matches are found, or a populated list 
        containing matching notes if one or more match is found.
        """
        # Return all notes containing 'text'
        matching_notes = []
        for note in self.notes:
            current_note = self.notes[note].get_text()
            # If there is a match, 'find' returns a positive integer
            if current_note.find(text) != (-1):
                matching_notes.append(self.notes[note])
        return matching_notes
    
    # Returns a note if it's index is stored, else returns None
    def search_note(self, note_index):
        return self.notes.get(note_index, None)
    
    def update_note(self, note_index, text):
        """
        Accepts 'note_index', a specific note position in the patient's 
        dictionary, and 'text', a new string to replace the old one with, as 
        inputs. Outputs False if the note does not exist, else outputs True. 
        """
        # Confirm the existance of the note at note_index
        if self.search_note(note_index) is None:
            print("Error: note does not exist")
            return False
        # Otherwise, update the note
        else:
            self.notes[note_index].revise_note(text)
            self.save_notes()
            return True
    
    def delete_note(self, note_index):
        """
        Accepts 'note_index', a specific note position in the patient's 
        dictionary, as input. Outputs False if the note does not exist, else
        outputs True.
        """
        # Confirm the note exists
        if self.search_note(note_index) is None:
            print("Error: note does not exist")
            return False
        # Delete the note
        else:
            self.autocounter -= 1            
            del self.notes[note_index]
            self.save_notes()
            return True
    
    def list_notes(self):
        """
        Creates, populates, and returns a list of all the notes associated
        with a particular Patient.
        """
        patient_note = []
        for note in reversed(self.notes):
            patient_note.append(self.notes[note])
        return patient_note

# ==============================================================================

def main():
    print("Main file called as 'note_dao_pickle.py'")

if __name__ == "__main__":
    main()

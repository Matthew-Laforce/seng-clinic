#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'note.py':

This file is re-used from assignment 4 with minimal alterations. The purpose of 
the note method is to initialize note objects. Note objects are used to store a 
note about a patient: they are held inside of a dictionary stored in the class 
'note_dao_pickle'.

============================================================================ """

# IMPORTS:
from datetime import datetime

class Note:
    def __init__(self, note_index, text):
        # Initialize note objects with an index and a string
        self.note_index = note_index
        self.text = text
        self.timestamp = datetime.now()
        
    def __str__(self):
        return f"\nTimestamp: {self.timestamp} \nNote index: {self.note_index} \nText: {self.text}"
        
    def __eq__(self, other):
        """
        Considers two note objects to be the same if their index and their
        string match. I intentionally do not check timestamps in equality 
        tests: this would be very difficult to incorporate into testing.
        """
        try:
            if self.note_index == other.note_index and self.text == other.text:
                return True
            else:
                return False
        except:
            return False
    
    def get_index(self):
        return self.note_index    
        
    def get_text(self):
        return self.text
    
    def get_timestamp(self):
        return self.timestamp
    
    # Updates the text in a 'note' object
    def revise_note(self, text):
        self.text = text
        self.timestamp = datetime.now()
        return

# ==============================================================================

def main():
    print("Main file called as 'note.py'.")

if __name__ == "__main__":
    main()

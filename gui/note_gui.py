#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'note_gui.py':

This file contains a series of classes which operate as GUI windows for
specific, note-related functions. For example, the SearchNote class creates
a standard search window which is re-purposed to handle a variety of note
searches. 

============================================================================ """

# EXCEPTIONS:
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
from clinic.exception.illegal_operation_exception import IllegalOperationException

# IMPORTS:
from PyQt6.QtCore import (
    pyqtSignal,
    QSize,
    Qt
)
from PyQt6.QtGui import (
    QAction,
    QIcon, 
    QPixmap
)
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStatusBar,
    QToolBar,
    QWidget
)
from clinic.controller import Controller
from clinic.note import Note
import os, sys

""" ======================================================================== """

class CreateUpdateNote(QMainWindow):
    """
    ============================================================================
    This class creates a GUI window that handles the creation and updating of 
    notes. It accepts a string, 'function', which tells it how to behave.
    ============================================================================
    """
    def __init__(self, caller, function, old_note):
        super().__init__()
        # Initialize variables
        self.controller = caller
        self.function = function
        self.old_note = old_note
        # Size the window, give it an icon
        self.setMinimumSize(400, 200)
        self.setWindowIcon(QIcon("clinic/gui/icons/mcs.png"))
        # Initialize a note creation or updating window
        if self.function == "create":
            self.setWindowTitle("Create Note")
        else:
            self.setWindowTitle("Update Note")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.create_layout = QGridLayout()
        central_widget.setLayout(self.create_layout)
        # Load GUI features
        self._load_gui()
        
    def _load_gui(self):
        # Create labels, text box for the window
        if self.function == "create":
            self.label_banner = QLabel("Please enter your note. \n")
            self.button_add = QPushButton("Add Note")
        else:
            self.label_banner = QLabel("Please enter a revised note. \n")
            self.button_add = QPushButton("Edit Note")
        self.text_note = QPlainTextEdit()
        # Position the labels and input boxes in a grid
        self.create_layout.addWidget(self.label_banner, 0, 0, 1, 4)
        self.create_layout.addWidget(self.text_note, 1, 0, 1, 4)
        # Include 'add note' (or edit) and 'cancel' buttons
        self.create_layout.addWidget(self.button_add, 2, 0, 1, 3)
        self.button_cancel = QPushButton("Cancel")
        self.create_layout.addWidget(self.button_cancel, 2, 3, 1, 1)
        # Disable the 'add' button until all fields have input
        self.button_add.setEnabled(False)
        # Connect the buttons and fields to signals
        self.text_note.textChanged.connect(self._fields_full)      
        self.button_add.clicked.connect(self._add_note)
        self.button_cancel.clicked.connect(self._cancel)
        # Pre-load the old note text if this class is used to 'update'
        if self.function == "update":
            self.text_note.appendPlainText(self.old_note.get_text())
        
    def _add_note(self):
        note = self.text_note.toPlainText().strip()
        if self.function == "create":
            self.controller.create_note(note)
            QMessageBox.information(self, "Success", "Note Created.")
        else:
            self.controller.update_note(self.old_note.get_index(), note)
            QMessageBox.information(self, "Success", "Note Updated.")
        self.close()
        
    def _cancel(self):
        self.close()

    # Disable note creation/edits when the text field is empty
    def _fields_full(self):
        if self.text_note.toPlainText().strip():
            self.button_add.setEnabled(True)
        else:
            self.button_add.setEnabled(False)


class SearchNote(QMainWindow):
    """
    ============================================================================
    This class creates a GUI window that handles note-related searches. It
    accepts a string, 'function', which tells it how to behave.
    ============================================================================
    """    
    def __init__(self, controller, caller, function):
        super().__init__()
        # Store the information from the 'caller'
        self.controller = controller
        self.caller = caller
        self.function = function
        # Size the window, give it a title and an icon
        self.setMinimumSize(200, 100)
        self.setWindowIcon(QIcon("clinic/gui/icons/mcs.png"))
        if self.function == "get":
            self.setWindowTitle("Get Note")
        elif self.function == "update":
            self.setWindowTitle("Update Note")
        elif self.function == "delete":
            self.setWindowTitle("Delete Note")
        else:
            self.setWindowTitle("Search Notes")
        # Initialize a search window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.create_layout = QGridLayout()
        central_widget.setLayout(self.create_layout)
        # Load GUI features
        self._load_gui()
        
    def _load_gui(self):
        # Create a text box for the window
        self.text_note_id = QLineEdit()        
        # Create labels for the window
        if self.function == "search":
            self.label_banner = QLabel("Please enter the keyword to search. (Input required) \n")
            self.label_note_id = QLabel("Keyword")
        else:
            self.label_banner = QLabel("Please enter the intended note ID. (Input required) \n")
            self.label_note_id = QLabel("Note ID")
            # Require PHN to be an integer (6 digits maximum)
            self.text_note_id.setInputMask('000000')            

        # Position the labels and input boxes in a grid
        self.create_layout.addWidget(self.label_banner, 0, 0, 1, 4)
        self.create_layout.addWidget(self.label_note_id, 1, 0, 1, 1)
        self.create_layout.addWidget(self.text_note_id, 1, 1, 1, 3)
        # Include 'search' (or similar) and 'cancel' buttons
        if self.function == "get":
            self.button_search = QPushButton("Get")
        elif self.function == "update":
            self.button_search = QPushButton("Update")
        elif self.function == "delete":
            self.button_search = QPushButton("Delete")
        else:
            self.button_search = QPushButton("Search")
        self.create_layout.addWidget(self.button_search, 2, 0, 1, 3)
        self.button_cancel = QPushButton("Cancel")
        self.create_layout.addWidget(self.button_cancel, 2, 3, 1, 1)
        # Disable the 'search' button until there is input
        self.button_search.setEnabled(False)
        # Connect the buttons and fields to signals
        self.text_note_id.textChanged.connect(self._fields_full)
        if self.function == "search":
            # Pass string searches back to 'main_menu_gui' with the text
            self.button_search.clicked.connect(self._search_text)
        else:
            # Other searches are handled internally in this GUI
            self.button_search.clicked.connect(self._search_id)
        self.button_cancel.clicked.connect(self._cancel)
        
    # Performs various note-ID related search operations
    def _search_id(self):
        note_id = int(self.text_note_id.text())
        note = self.controller.search_note(note_id)
        if note is not None:
            if self.function == "get":
                QMessageBox.information(self, "Result", f"Note found: {note}")
            elif self.function == "update":
                QMessageBox.information(self, "Result", "Note Found.")
                self.update_note_window = CreateUpdateNote(self.controller, \
                                                           "update", note)
                self.update_note_window.show()            
            else:
                self.delete_window = ConfirmDeleteNote(self.controller, note_id)
                self.delete_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Result", "No note found with that ID.")
        self.text_note_id.clear()
        
    # Performs keyword based search operations
    def _search_text(self):
        result = self.text_note_id.text()
        self.caller.search_note_results(result)
        QMessageBox.information(self, "Result", "Showing Matches.")
        self.close()
        
    def _cancel(self):
        self.close()
        
    # Disable searches until the user adds input to the field
    def _fields_full(self):
        if self.text_note_id.text():
            self.button_search.setEnabled(True)
        else:
            self.button_search.setEnabled(False)

class ConfirmDeleteNote(QMainWindow):
    def __init__(self, caller, note_id):
        super().__init__()
        # Get the controller and phn from the caller
        self.controller = caller
        self.note_id = note_id
        # Create the window
        self.setWindowTitle("Confirm Deletion")
        self.setWindowIcon(QIcon("clinic/gui/icons/mcs.png"))
        self.setMinimumSize(200, 100)
        # Initialize a deletion verification
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.create_layout = QGridLayout()
        central_widget.setLayout(self.create_layout)
        # Load GUI features
        self._load_gui()
        
    def _load_gui(self):
        # Create labels for the window
        self.label_banner = QLabel(f"The following note was located: {self.controller.search_note(self.note_id)};\nReally delete? \n")
        self.create_layout.addWidget(self.label_banner, 0, 0, 1, 4)
        # Include 'search' and 'cancel' buttons
        self.button_delete = QPushButton("Delete")
        self.create_layout.addWidget(self.button_delete, 1, 0, 1, 3)
        self.button_cancel = QPushButton("Cancel")
        self.create_layout.addWidget(self.button_cancel, 1, 3, 1, 1)
        # Connect the buttons and fields to signals
        self.button_delete.clicked.connect(self._delete)
        self.button_cancel.clicked.connect(self._cancel)
        
    def _delete(self):
        self.controller.delete_note(self.note_id)
        QMessageBox.information(self, "Result", f"Note deleted.")
        self.close()
        
    def _cancel(self):
        self.close()

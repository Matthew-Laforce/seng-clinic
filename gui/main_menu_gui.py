#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'main_menu_gui.py':

This code contains the methods used to initialize the GUI's main menu. The
login and logout GUIs are handled in 'clinic_gui.py', while patient and note
GUIS are handled in 'patient_gui.py' and 'note_gui.py' respectively.

============================================================================ """

# EXCEPTIONS
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException

# IMPORTS
from PyQt6.QtCore import (
    QSize,
    Qt
)
from PyQt6.QtGui import (
    QAction,
    QIcon, 
    QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTableView,
    QToolBar,
    QWidget,
    QWidgetAction,
)
import sys, os
from clinic.controller import Controller
from clinic.gui.note_gui import *
from clinic.gui.patient_gui import *

# General GUI Stuff:
""" ======================================================================== """

class MainMenuGUI(QMainWindow):
    def __init__(self, caller, controller):
        super().__init__()
        self.caller = caller
        self.controller = controller
        self.label_banner = None
        # General GUI settings for the main menu
        self.setStatusBar(QStatusBar(self))
        self.setWindowTitle("MCS - Medical Clinic System")
        self.setWindowIcon(QIcon("clinic/gui/icons/mcs.png"))
        self.setMinimumSize(800, 600)
        # Create a placeholder label (replace with actual menu components later)
        self.label = QLabel("Welcome to the MCS - Medical Clinic System!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Add and populate a menu bar
        self.menu = self.menuBar()
        self.menu_bar_data()
        self.menu_bar_patient()
        self.menu_bar_note()
        self.menu_bar_logout()
        # Set the central widget
        self.widget = QWidget()
        self.layout = QGridLayout()
        self.layout.addWidget(self.label)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        # Add a bar for the current patient
        self.current_patient_bar()


    def menu_bar_data(self):
        """
        =======================================================================
        Adds 'data' menu and patient-admin functions to the toolbar.
        =======================================================================
        """
        objects_menu = self.menu.addMenu("&Data")
        # Search Patient Action
        search_patient_action = QAction("&Search PHN", self)
        search_patient_action.setStatusTip("Search Database for PHN")
        search_patient_action.triggered.connect(self.search_patient_phn_gui)
        objects_menu.addAction(search_patient_action)        
        # Retrieve Patients Action
        retrieve_patients_action = QAction("&Search Name", self)
        retrieve_patients_action.setStatusTip("Search Database for Name")
        retrieve_patients_action.triggered.connect(self.search_patient_name_gui)
        objects_menu.addAction(retrieve_patients_action)
        objects_menu.addSeparator()
        # List Patient Action
        list_patient_action = QAction("&List Patients", self)
        list_patient_action.setStatusTip("List all Patients in Database")
        list_patient_action.triggered.connect(self.list_patient_gui)
        objects_menu.addAction(list_patient_action)         


    def menu_bar_patient(self):
        """
        =======================================================================
        Add the ability to 'set' and 'unset' patients to the toolbar.
        =======================================================================
        """
        objects_menu = self.menu.addMenu("&Patient")
        # Create Patient Action
        create_patient_action = QAction("&Add Patient", self)
        create_patient_action.setStatusTip("Add Patient to Database")
        create_patient_action.triggered.connect(self.create_patient_gui)
        objects_menu.addAction(create_patient_action)
        # Update Patient Action
        update_patient_action = QAction("&Update Patient", self)
        update_patient_action.setStatusTip("Update Patient Information")
        update_patient_action.triggered.connect(self.update_patient_gui)
        objects_menu.addAction(update_patient_action)
        # Delete Patient Action
        delete_patient_action = QAction("&Delete Patient", self)
        delete_patient_action.setStatusTip("Remove Patient From Database")
        delete_patient_action.triggered.connect(self.delete_patient_gui)
        objects_menu.addAction(delete_patient_action)
        objects_menu.addSeparator()        
        # Set Patient Action
        set_patient_action = QAction("&Set Patient", self)
        set_patient_action.setStatusTip("Select Patient by PHN")
        set_patient_action.triggered.connect(self.set_patient_gui)
        objects_menu.addAction(set_patient_action)
        # Unset Patient Action
        unset_patient_action = QAction("&Unset Patient", self)
        unset_patient_action.setStatusTip("Un-select Current Patient")
        unset_patient_action.triggered.connect(self.unset_patient_gui)
        objects_menu.addAction(unset_patient_action)        


    def menu_bar_note(self):
        """
        =======================================================================
        Adds a 'note' menu and related functions to the toolbar
        =======================================================================
        """
        objects_menu = self.menu.addMenu("&Note")
        # Create Note Action
        create_note_action = QAction("&New Note", self)
        create_note_action.setStatusTip("Create a new Patient Note (Requires a Current Patient)")
        create_note_action.triggered.connect(self.new_note_gui)
        objects_menu.addAction(create_note_action)
        # Update Note Action
        update_note_action = QAction("&Update Note", self)
        update_note_action.setStatusTip("Change an Existing Note (Requires a Current Patient)")
        update_note_action.triggered.connect(self.update_note_gui)
        objects_menu.addAction(update_note_action)
        objects_menu.addSeparator()
        # List Note Action
        list_note_action = QAction("List Notes", self)
        list_note_action.setStatusTip("Shows all Patient Notes (Requires a Current Patient)")
        list_note_action.triggered.connect(self.list_notes_gui)
        objects_menu.addAction(list_note_action)
        # Search Note Action
        search_note_action = QAction("&Search Notes", self)
        search_note_action.setStatusTip("Search Existing Notes for a Keyword (Requires a Current Patient)")
        search_note_action.triggered.connect(self.search_note_gui)
        objects_menu.addAction(search_note_action)
        # Retrieve Note Action
        retrieve_note_action = QAction("&Get Note", self)
        retrieve_note_action.setStatusTip("Find an Existing Note By ID (Requires a Current Patient)")
        retrieve_note_action.triggered.connect(self.retrieve_note_gui)
        objects_menu.addAction(retrieve_note_action)
        objects_menu.addSeparator()
        # Delete Note Action
        delete_note_action = QAction("&Delete Note", self)
        delete_note_action.setStatusTip("Remove an Existing Note (Requires a Current Patient)")
        delete_note_action.triggered.connect(self.delete_note_gui)
        objects_menu.addAction(delete_note_action)

    # Add a logout button to the toolbar
    def menu_bar_logout(self):
        logout_action = QAction("&Logout", self)
        logout_action.setStatusTip("Log out of the MCS")
        logout_action.triggered.connect(self.caller.logout_button_clicked)
        self.menu.addAction(logout_action)

    # Load a display banner into the GUI
    def create_banner(self):
        self.label_banner = QLabel()
        self.label_banner.setFrameShape(QFrame.Shape.Box)
        self.label_banner.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.label_banner, 0, 0, 1, 4)
        
    # Function-specific stuff:
    """ ==================================================================== """    

    # USER STORY 2 - Logout
    def logout(self):
        self.label_banner = None
        self.controller.unset_current_patient()
        self.patient_bar.close()
        self.current_patient_bar()
        self.controller.logout()  
        

    # USER STORY 3 - Search Patient (PHN search)
    def search_patient_phn_gui(self):
        self.search_patient_window = SearchNamePHN(self.controller, self, "search")      
        self.search_patient_window.show()    


    # USER STORY 4 - Create Patient
    def create_patient_gui(self):
        self.create_patient_window = CreateUpdatePatient(self.controller, "add")      
        self.create_patient_window.show()


    # USER STORY 5 - Retrieve Patient (name search)
    def search_patient_name_gui(self):
        self.search_name_window = SearchNamePHN(self.controller, self, "name")
        self.search_name_window.show()

    def search_name_results(self, matches, name):
        # Clear the current contents from the main window
        self.label.hide()
        # Update the menu with search info
        if self.label_banner is None:
            self.create_banner()
        self.label_banner.setText(f"\nShowing {len(matches)} result(s) for search \"{name}\".\n")
        # Position the names in a grid
        self.patient_table = QTableView()
        self.model = TableModel(matches)    
        self.patient_table.setModel(self.model)
        self.patient_table.resizeColumnsToContents()
        self.layout.addWidget(self.patient_table, 1, 0, 1, 4)


    # USER STORY 6 - Update Patient
    def update_patient_gui(self):
        self.update_patient_window = SearchNamePHN(self.controller, self, \
                                                   "update")
        self.update_patient_window.show()    


    # USER STORY 7 - Delete Patient
    def delete_patient_gui(self):
        self.delete_patient_window = DeletePatient(self.controller)
        self.delete_patient_window.show()


    # USER STORY 8 - List Patients
    def list_patient_gui(self):
        # Get patient list
        patient_list = self.controller.list_patients()
        # Clear the current contents from the main window
        self.label.hide()
        # Update the menu with search info
        if self.label_banner is None:
            self.create_banner()
        self.label_banner.setText(f"\nShowing all patients \nResults found: {len(patient_list)}.\n")
        # Position the names in a grid
        self.patient_table = QTableView()
        self.model = TableModel(patient_list)    
        self.patient_table.setModel(self.model)
        self.patient_table.resizeColumnsToContents()
        self.layout.addWidget(self.patient_table, 1, 0, 1, 4)            


    # USER STORY 9 - Set / Unset Patient
    def current_patient_bar(self):
        patient_text = self.controller.current_patient
        if patient_text is None:
            patient_bar_text = "Current Patient: \nNone"
        else:
            patient_bar_text = "Current Patient: " + str(patient_text)
        self.patient_bar = QLabel(patient_bar_text)
        self.patient_bar.setFrameShape(QFrame.Shape.Box)
        self.patient_bar.setStyleSheet("padding: 5px;")
        # Shrink the bar when able, then initialize
        self.patient_bar.setSizePolicy(QSizePolicy.Policy.Expanding,\
                                       QSizePolicy.Policy.Fixed)
        self.layout.addWidget(self.patient_bar)        

    def set_patient_gui(self):
        self.set_patient_window = SearchNamePHN(self.controller, self, "set")
        self.set_patient_window.show()

    def unset_patient_gui(self):
        if self.controller.get_current_patient() is None:
            QMessageBox.critical(self, "Error", "No patient selected.")
        else:
            QMessageBox.information(self, "Result", "Patient Unset.")
            self.controller.unset_current_patient()
            self.patient_bar.close()
            self.current_patient_bar()


    # USER STORY 10 - Create Note
    def new_note_gui(self):
        try:
            self.controller.check_current_exists()
            self.new_note_window = CreateUpdateNote(self.controller, "create", None)
            self.new_note_window.show()
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No patient selected.")


    # USER STORY 11 - Retrieve Notes (text) / Search Notes (PHN)
    def retrieve_note_gui(self):
        try:
            self.controller.check_current_exists()
            self.retrieve_note_window = SearchNote(self.controller, self, "get")      
            self.retrieve_note_window.show()
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No patient selected.")    

    def search_note_gui(self):
        try:
            self.controller.check_current_exists()
            self.retrieve_note_window = SearchNote(self.controller, self, \
                                                   "search")      
            self.retrieve_note_window.show()
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No patient selected.")

    def search_note_results(self, search_string):
        # Clear the current contents from the main window
        self.label.hide()
        # Get patient information as context for the next menu
        patient = self.controller.get_current_patient()
        patient_name = patient.get_name()
        patient_phn = patient.get_phn()
        # Get a list of notes containing 'search_string'
        note_list = self.controller.retrieve_notes(search_string)        
        # Update the menu with patient info
        if self.label_banner is None:
            self.create_banner()        
        self.label_banner.setText(f"\nShowing notes for {patient_name} (PHN: {patient_phn}) \nSearch term: \"{search_string}\" \nResults found: {len(note_list)}\n")
        # Put the patient info into a box
        self.label_banner.setFrameShape(QFrame.Shape.Box)
        self.label_banner.setStyleSheet("padding: 5px;")
        # Position the banner and the search results
        self.text_note = QPlainTextEdit()
        self.layout.addWidget(self.label_banner, 0, 0, 1, 4)
        self.layout.addWidget(self.text_note, 1, 0, 1, 4)  
        # Print the matching notes
        for note in note_list:
            self.text_note.appendPlainText(str(note.get_timestamp()))
            self.text_note.appendPlainText(f"Index: {note.get_index()}")
            self.text_note.appendPlainText(f"{note.get_text()} \n")
        self.text_note.setReadOnly(True)            
        self.notes_shown = True


    # USER STORY 12 - Update Note
    def update_note_gui(self):
        try:
            self.controller.check_current_exists()
            self.update_note_window = SearchNote(self.controller, self, \
                                                 "update")
            self.update_note_window.show()
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No patient selected.")


    # USER STORY 13 - Delete Note
    def delete_note_gui(self):
        try:
            self.controller.check_current_exists()
            self.delete_note_window = SearchNote(self.controller, self, \
                                                 "delete")
            self.delete_note_window.show()
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No patient selected.")      


    # USER STORY 14 - List Notes
    def list_notes_gui(self):
        if self.controller.current_patient is None:
            QMessageBox.critical(self, "Error", "No patient selected.")
        else:
            # Clear the current contents from the main window
            self.label.hide()
            # Get patient information as context in the next menu
            patient = self.controller.get_current_patient()
            patient_name = patient.get_name()
            patient_phn = patient.get_phn()
            # Get a list of all the notes
            note_list = self.controller.list_notes()
            # Update the menu with patient info
            if self.label_banner is None:
                self.create_banner()
            self.label_banner.setText(f"\nShowing all notes for {patient_name} (PHN: {patient_phn}) \nResults found: {len(note_list)}\n")
            # Position the notes in a grid
            self.text_note = QPlainTextEdit()
            self.layout.addWidget(self.text_note, 1, 0, 1, 4)            
            # Print all the notes
            for note in note_list:
                self.text_note.appendPlainText(str(note.get_timestamp()))
                self.text_note.appendPlainText(f"Index: {note.get_index()}")
                self.text_note.appendPlainText(f"{note.get_text()} \n")
            self.text_note.setReadOnly(True)            
            self.notes_shown = True

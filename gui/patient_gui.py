#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'patient_menu_gui.py':

This file contains a series of classes which operate as GUI windows for
specific, patient-related functions. For example, the SearchNamePHN class 
creates a standard search window which is re-purposed to handle a variety of
patient searches. 

============================================================================ """

# EXCEPTIONS:
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
from clinic.exception.illegal_operation_exception import IllegalOperationException

# IMPORTS:
from PyQt6 import QtCore
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
    QPushButton,
    QStatusBar,
    QToolBar,
    QWidget
)
from clinic.controller import Controller
from clinic.patient import Patient

""" ======================================================================== """

class CreateUpdatePatient(QMainWindow):
    """
    ============================================================================
    This class creates a GUI window which handles the creation and updating of 
    patients. It accepts a string, 'function', which tells it how to behave.
    ============================================================================
    """
    def __init__(self, caller, function):
        super().__init__()
        self.function = function
        self.controller = caller
        # Change window title depending on how the class is called
        if self.function == "add":
            self.setWindowTitle("Add Patient")
        else:
            self.setWindowTitle("Update Patient")
        # Size the window, give it an icon
        self.setMinimumSize(400, 200)
        self.setWindowIcon(QIcon("clinic/gui/icons/mcs.png"))
        # Initialize a patient creation window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.create_layout = QGridLayout()
        central_widget.setLayout(self.create_layout)
        # Load GUI features
        self._load_gui()
        
    def _load_gui(self):
        # Create labels for the window
        self.label_banner = QLabel("Please input new patient information. (All fields required) \n")
        self.label_phn = QLabel("PHN")
        self.label_name = QLabel("Name")
        self.label_birth = QLabel("Birth Date")
        self.label_phone = QLabel("Phone Number   ")
        self.label_email = QLabel("Email")
        self.label_address = QLabel("Address")
        # Create text boxes for the window
        self.text_phn = QLineEdit()
        self.text_name = QLineEdit()
        self.text_birth = QLineEdit()
        self.text_phone = QLineEdit()
        self.text_email = QLineEdit()
        self.text_address = QLineEdit()
        # Require PHN to be an integer (12 digits maximum)
        self.text_phn.setInputMask('000000000000')
        # Position the labels and input boxes in a grid
        self.create_layout.addWidget(self.label_banner, 0, 0, 1, 4)
        self.create_layout.addWidget(self.label_phn, 1, 0, 1, 1)
        self.create_layout.addWidget(self.text_phn, 1, 1, 1, 3)
        self.create_layout.addWidget(self.label_name, 2, 0, 1, 1)
        self.create_layout.addWidget(self.text_name, 2, 1, 1, 3)
        self.create_layout.addWidget(self.label_birth, 3, 0, 1, 1)
        self.create_layout.addWidget(self.text_birth, 3, 1, 1, 3)
        self.create_layout.addWidget(self.label_phone, 4, 0, 1, 1)
        self.create_layout.addWidget(self.text_phone, 4, 1, 1, 3)
        self.create_layout.addWidget(self.label_email, 5, 0, 1, 1)
        self.create_layout.addWidget(self.text_email, 5, 1, 1, 3)
        self.create_layout.addWidget(self.label_address, 6, 0, 1, 1)
        self.create_layout.addWidget(self.text_address, 6, 1, 1, 3)
        # Include 'add' (or update) and 'cancel' buttons
        if self.function == "add":
            self.button_add = QPushButton("Add")
        else:
            self.button_add = QPushButton("Update")
        self.create_layout.addWidget(self.button_add, 7, 0, 1, 3)
        self.button_cancel = QPushButton("Cancel")
        self.create_layout.addWidget(self.button_cancel, 7, 3, 1, 1)
        # Disable the 'add' button until all fields have input
        self.button_add.setEnabled(False)
        # Connect the buttons and fields to signals
        self.text_phn.textChanged.connect(self._fields_full)
        self.text_name.textChanged.connect(self._fields_full)
        self.text_birth.textChanged.connect(self._fields_full)
        self.text_phone.textChanged.connect(self._fields_full)
        self.text_email.textChanged.connect(self._fields_full)
        self.text_address.textChanged.connect(self._fields_full)        
        self.button_add.clicked.connect(self._patient)
        self.button_cancel.clicked.connect(self._cancel)
        # If 'update patient' is called, pre-load patient information
        if self.function != "add":
            self.text_phn.setText(str(self.function.get_phn()))
            self.text_name.setText(self.function.get_name())
            self.text_birth.setText(self.function.get_birthdate())
            self.text_phone.setText(self.function.get_phone())
            self.text_email.setText(self.function.get_email())
            self.text_address.setText(self.function.get_address())

    def _patient(self):
        phn = int(self.text_phn.text())
        name = self.text_name.text().strip()
        birth = self.text_birth.text().strip()
        phone = self.text_phone.text().strip()
        email = self.text_email.text().strip()
        address = self.text_address.text().strip()
        if self.function == "add":
            try:
                self.controller.create_patient(phn, name, birth, phone, email, address)
                QMessageBox.information(self, "Success", "Patient Creation Successful.")
                self.close()                
            except IllegalOperationException:
                QMessageBox.critical(self, "Error", "PHN in use.")
        else:
            try:
                self.old_phn = int(self.function.get_phn())
                self.controller.update_patient(self.old_phn, phn, name, birth, phone, email, address)
                QMessageBox.information(self, "Success", "Patient Updated.")
                self.close()
            except IllegalOperationException:
                QMessageBox.critical(self, "Error", "PHN in use.")
        
    def _cancel(self):
        self.close()
        
    # Disable 'submit' button until all fields are populated
    def _fields_full(self):
        if self.text_phn.text() and self.text_name.text() and \
           self.text_birth.text() and self.text_phone.text() and \
           self.text_email.text() and self.text_address.text():
            self.button_add.setEnabled(True)
        else:
            self.button_add.setEnabled(False)


class SearchNamePHN(QMainWindow):
    """
    ============================================================================
    This class creates a GUI window which handles patient related searches with
    respect to either a name string or a PHN integer. The specifics are decided
    by the 'function' string. 
    ============================================================================
    """    
    def __init__(self, controller, caller, function):
        super().__init__()
        self.controller = controller
        self.caller = caller
        self.function = function
        # Create the window
        self.setWindowIcon(QIcon("clinic/gui/icons/mcs.png"))
        if self.function == "search":
            self.setWindowTitle("Find PHN")
        elif self.function == "set":
            self.setWindowTitle("Set Patient")
        elif self.function == "update":
            self.setWindowTitle("Update Patient")
        else:
            self.setWindowTitle("Search Name")
        self.setMinimumSize(200, 100)
        # Initialize a search window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.create_layout = QGridLayout()
        central_widget.setLayout(self.create_layout)
        # Load GUI features
        self._load_gui()
        
    def _load_gui(self):
        # Create a text box for the window
        self.text_phn = QLineEdit()        
        # Create labels for the window
        if self.function != "name":
            # Customize the window for PHN search
            self.label_banner = QLabel("Please enter the desired PHN. (Input required) \n")
            self.label_phn = QLabel("PHN")
            self.text_phn.setInputMask('000000000000')
        else: 
            # Design the window for name search
            self.label_banner = QLabel("Please enter the name to search. (Input required)\n")
            self.label_phn = QLabel("Name")
        # Position the labels and input boxes in a grid
        self.create_layout.addWidget(self.label_banner, 0, 0, 1, 4)
        self.create_layout.addWidget(self.label_phn, 1, 0, 1, 1)
        self.create_layout.addWidget(self.text_phn, 1, 1, 1, 3)
        # Include 'search' and 'cancel' buttons
        if self.function == "search":
            self.button_search = QPushButton("Find PHN")
        elif self.function == "set":
            self.button_search = QPushButton("Set")
        elif self.function == "update":
            self.button_search = QPushButton("Update")
        else:
            self.button_search = QPushButton("Find Name")
        self.create_layout.addWidget(self.button_search, 2, 0, 1, 3)
        self.button_cancel = QPushButton("Cancel")
        self.create_layout.addWidget(self.button_cancel, 2, 3, 1, 1)
        # Disable the 'search' button until there is input
        self.button_search.setEnabled(False)
        # Connect the buttons and fields to signals
        self.text_phn.textChanged.connect(self._fields_full)
        if self.function != "name":
            self.button_search.clicked.connect(self._search_phn)
        else:
            self.button_search.clicked.connect(self._search_name)
        self.button_cancel.clicked.connect(self._cancel)
        
    # Handle PHN-based searches
    def _search_phn(self):
        phn = int(self.text_phn.text())
        patient = self.controller.search_patient(phn)
        if patient is not None:
            if self.function == "search":
                QMessageBox.information(self, "Result", f"Patient found: {patient}")
            elif self.function == "set":
                QMessageBox.information(self, "Result", "Patient Set.")
                phn = int(patient.get_phn())
                self.controller.set_current_patient(phn)
                self.caller.patient_bar.close()
                self.caller.current_patient_bar()
            else:
                try:
                    self.controller.is_current_patient(phn)
                    QMessageBox.information(self, "Result", "Patient Found.")
                    self.update_patient_window = CreateUpdatePatient(self.controller, patient)
                    self.update_patient_window.show()
                except IllegalOperationException:
                    QMessageBox.critical(self, "Error", "Cannot update the current patient")
            self.close()
        else:
            QMessageBox.critical(self, "Result", "No patient found with that PHN.")
        self.text_phn.clear()
    
    # Handle string-based searches
    def _search_name(self):
        # Plug name into 'retrieve patients', make a match list
        name = self.text_phn.text().strip()
        matches = self.controller.retrieve_patients(name)
        # Return the list of matches
        QMessageBox.information(self, "Result", f"Found {len(matches)} Match(es).")
        self.caller.search_name_results(matches, name)
        self.close()
        
    def _cancel(self):
        self.close()
        
    # Confirm the user gives the function something to search with first
    def _fields_full(self):
        if self.text_phn.text():
            self.button_search.setEnabled(True)
        else:
            self.button_search.setEnabled(False)


class DeletePatient(QMainWindow):
    """
    ============================================================================
    This class creates a GUI window which handles patient deletion. The basic
    idea here is to get a PHN and to confirm the user wants to delete the
    patient.
    ============================================================================
    """       
    def __init__(self, caller):
        super().__init__()
        self.controller = caller
        # Create the window
        self.setWindowTitle("Delete Patient")
        self.setWindowIcon(QIcon("clinic/gui/icons/mcs.png"))
        self.setMinimumSize(200, 100)
        # Initialize a search window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.create_layout = QGridLayout()
        central_widget.setLayout(self.create_layout)
        # Load GUI features
        self._load_gui()
        
    def _load_gui(self):
        # Create labels for the window
        self.label_banner = QLabel("Please enter a PHN to search. (Input required) \n")
        self.label_phn = QLabel("PHN")
        # Create text boxes for the window
        self.text_phn = QLineEdit()
        # Require PHN to be an integer (12 digits maximum)
        self.text_phn.setInputMask('000000000000')
        # Position the labels and input boxes in a grid
        self.create_layout.addWidget(self.label_banner, 0, 0, 1, 4)
        self.create_layout.addWidget(self.label_phn, 1, 0, 1, 1)
        self.create_layout.addWidget(self.text_phn, 1, 1, 1, 3)
        # Include 'search' and 'cancel' buttons
        self.button_search = QPushButton("Search")
        self.create_layout.addWidget(self.button_search, 2, 0, 1, 3)
        self.button_cancel = QPushButton("Cancel")
        self.create_layout.addWidget(self.button_cancel, 2, 3, 1, 1)
        # Disable the 'add' button until all fields have input
        self.button_search.setEnabled(False)
        # Connect the buttons and fields to signals
        self.text_phn.textChanged.connect(self._fields_full)    
        self.button_search.clicked.connect(self._search)
        self.button_cancel.clicked.connect(self._cancel)
        
    # Find the patient then confirm deletion
    def _search(self):
        phn = int(self.text_phn.text())
        patient = self.controller.search_patient(phn)
        if patient is not None:
            try:
                self.controller.is_current_patient(phn)
                self.confirm_delete = ConfirmDeletePatient(self.controller, phn)      
                self.confirm_delete.show()
                self.close()
            except IllegalOperationException:
                QMessageBox.critical(self, "Error", "Cannot delete the 'current patient'.")
        else:
            QMessageBox.critical(self, "Error", "No patient found with that PHN.")
        self.text_phn.clear()
        
    def _cancel(self):
        self.close()
        
    # Force input to be provided before the user can delete anything
    def _fields_full(self):
        if self.text_phn.text():
            self.button_search.setEnabled(True)
        else:
            self.button_search.setEnabled(False)
            
            
class ConfirmDeletePatient(QMainWindow):
    """
    ============================================================================
    This is a helper class for 'DeletePatient', it performs a second check
    to confirm deletion before removing a patient from the system.
    ============================================================================
    """      
    def __init__(self, caller, phn):
        super().__init__()
        self.controller = caller
        self.phn = phn
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
        self.label_banner = QLabel(f"A patient has been found with the PHN {self.phn}. Really delete? \n")
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
        self.controller.delete_patient(self.phn)
        QMessageBox.information(self, "Result", f"Patient deleted.")
        self.close()
        
    def _cancel(self):
        self.close()
        

class TableModel(QtCore.QAbstractTableModel):
    """
    ============================================================================
    This TableModel class is used with 'Search Name' and 'List Patients' to
    create a patient table.
    ============================================================================
    """
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.headers = ["PHN", "Name", "Birth Date", "Phone", "Email",\
                        "Address"]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # Get the Patient for the row
            patient = self.data[index.row()]
            column = index.column()
            # Map the columns to Patient variables
            if column == 0:
                return patient.phn
            elif column == 1:
                return patient.name
            elif column == 2:
                return patient.birth_date
            elif column == 3:
                return patient.phone
            elif column == 4:
                return patient.email
            elif column == 5:
                return patient.address

    def rowCount(self, index):
        # The length of the outer list.
        return len(self.data)

    def columnCount(self, index):
        # Count of the printable variables for each patient
        return len(self.headers)
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role ==\
           Qt.ItemDataRole.DisplayRole:
            # Return the column headers
            return self.headers[section]
        return super().headerData(section, orientation, role)
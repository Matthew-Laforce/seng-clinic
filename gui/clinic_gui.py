#!/usr/bin/env python3
""" ============================================================================

SENG 265 -- Assignment 5
Matthew Laforce
V01019219
Created Nov 28, 2024

'clinic_gui.py':

This code acts as a 'starting point' for the MCS: on successful login, it hides 
itself and shows a 'MainMenuGUI'. Login and logout GUI tasks are handled
here; other GUI logic is handled in either main_menu_gui.py, note_gui.py, or
patient_gui.py.

============================================================================ """

# IMPORTS
from PyQt6.QtCore import pyqtSignal, Qt 
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QWidget,
)
import sys, os
from clinic.controller import Controller
from clinic.gui.main_menu_gui import MainMenuGUI

""" ======================================================================== """

class ClinicGUI(QDialog):
    """
    ============================================================================
    This class initializes a login screen for the MCS. After the user logs
    in, the screen closes and directs the user to the main screen.
    ============================================================================
    """
    def __init__(self):
        # Initialize the program
        super().__init__()
        self.controller = Controller(autosave=True)
        # Pass controller to the main menu GUI
        self.main_menu_gui = MainMenuGUI(self, self.controller)
        # General GUI settings for the login window
        self.setWindowTitle("MCS Login - Medical Clinic System")
        self.setWindowIcon(QIcon("clinic/gui/icons/mcs.png"))
        self.setMinimumSize(400, 130)
        # Use a grid-based layout
        layout = QGridLayout()
        # Create user box in the login window
        label_username = QLabel("Username")
        layout.addWidget(label_username, 0, 0)
        self.text_username = QLineEdit()
        layout.addWidget(self.text_username, 1, 0)
        # Create a password box in the login window
        label_password = QLabel("Password")
        layout.addWidget(label_password, 2, 0)
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)        
        layout.addWidget(self.text_password, 3, 0)
        # Add a login button
        self.button_login = QPushButton("Login")
        layout.addWidget(self.button_login, 4, 0)        
        # Create a lock icon
        lock_icon_label = QLabel()
        lock_pixmap = QPixmap("clinic/gui/icons/lock.png")
        lock_icon_label.setPixmap(lock_pixmap)
        layout.addWidget(lock_icon_label, 0, 1, 5, 1)        
        # Set the layout
        self.setLayout(layout)
        # Connect the button's signal to the slot
        self.button_login.clicked.connect(self.login_button_clicked)

    def login_button_clicked(self):
        # Get the username and password from the widgets
        username = self.text_username.text()
        password = self.text_password.text()
        try:
            if self.controller.login(username, password) is True:
                self.main_menu_gui.show()
                self.hide()
                QMessageBox.information(self, "Success", "Login Successful.")
            else:
                QMessageBox.critical(self, "Error", "Invalid login information.")
        except:
            QMessageBox.critical(self, "Error", "Login Failed.")
        # After the login, clear the text from the text widgets
        self.text_username.clear()
        self.text_password.clear()
        
    def logout_button_clicked(self):
        self.logout_confirmed = ConfirmLogout()
        self.logout_confirmed.logout_decision.connect(self._handle_logout)
        self.logout_confirmed.show()
            
    def _handle_logout(self, confirmed):
        if confirmed is True:
            self.main_menu_gui.logout()       
            self.main_menu_gui.close()
            self.main_menu_gui.deleteLater()
            self.main_menu_gui = MainMenuGUI(self, self.controller)
            self.show()


class ConfirmLogout(QMainWindow):
    """
    ============================================================================
    This class verifies the user's logout before actually performing the action.
    Confirmation is sent back to the related functions in the 'MainMenuGUI'.
    ============================================================================
    """
    logout_decision = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Confirm Logout")
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
        self.label_banner = QLabel(f"Really log out? \n")
        self.create_layout.addWidget(self.label_banner, 0, 0, 1, 4)
        # Include 'log out' and 'cancel' buttons
        self.button_logout = QPushButton("Log Out")
        self.create_layout.addWidget(self.button_logout, 1, 0, 1, 3)
        self.button_cancel = QPushButton("Cancel")
        self.create_layout.addWidget(self.button_cancel, 1, 3, 1, 1)
        # Connect the buttons and fields to signals
        self.button_logout.clicked.connect(self._confirmed_logout)
        self.button_cancel.clicked.connect(self._cancel)
        
    def _confirmed_logout(self):
        self.logout_decision.emit(True)
        self.close()
        
    def _cancel(self):
        self.logout_decision.emit(False)
        self.close()

""" ======================================================================== """

def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()

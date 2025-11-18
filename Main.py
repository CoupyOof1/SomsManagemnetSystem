#region Imports List
import sys # interacting with the laptop system 
import csv # Importing csv library for extracting and using data from the csv file 

#       IMPORTING PYQT5 LIBRARY FOR GUI INTERFACE 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QListWidget, QVBoxLayout, QListWidgetItem, QLabel, QHBoxLayout, QPushButton, QStackedWidget
#endregion 
#region File Imports 
from Dashboard import * 
from Account import *
from Property import *
from SearchFilter import *
#endregion

#      EXPLAINATION
"""
    I started with the main window application window, establisshing the system's foundation
    for Soms Management using the PyQt5 framework. It began with theimports of essential python
    libraries like sys and csv for system and data handling, tagged alongside with Pyqt5 components
    for building its graphical user interface. The main class downbelow will inherit from the QMain
    -Window and will be responsible for intializing and configuring the window' title, positipon and
    dimensions. Along side with a QStackedWidget created for managing multiple users interface screens
    , smooth navigation between different views like login, registeration, dashboard, etc. Overall, this
    code establishes the system's structual framework and interface navigation serving as the core platform
    for integrating property management features.
"""

#region MainWindow Application 
class SomsManagementLoginSystem(QMainWindow): 
    #region Initialisation 
    def __init__(self):
        super().__init__() # Intializing the class

        #      (WINDOW PROPERTIES)
        # - Changeable properties for manipulating the exact dimensions of a window 
        self.WDW_Xpos = 100   # X position 
        self.WDW_Ypos = 100   # Y Position 
        self.WDW_Width = 760  # WIDTH 760
        self.WDW_Height = 560 # HEIGHT 700

        #      (SETUP WINDOW)
        # - Code down below will setup and determine the window's title and position and scale measurements 
        self.setWindowTitle("SomsManagement by Coupy")                                  # Setting up window title
        self.setGeometry(self.WDW_Xpos, self.WDW_Ypos, self.WDW_Width, self.WDW_Height) # Registering the scale

        #      (SETUP ALL SCREENS)
        self.MAIN_WIDGET = QStackedWidget()     # Creating QStackedWidget for holding all screens
        self.setCentralWidget(self.MAIN_WIDGET) # Makes this class the central widget of the QMainApplication

        #      [CREATE SCENES]
        # - Creating each screen for corresponding class
        self.SCRN_loginacc = LoginAcc_Screen(self.MAIN_WIDGET)
        self.SCRN_registeracc = RegisterAcc_Screen(self.MAIN_WIDGET)
        self.SCRN_verifyacc = VerifyAcc_Screen(self.MAIN_WIDGET, None, None, None, None)
        self.SCRN_dashboard = AdminDashboard_Screen(self.MAIN_WIDGET, None)
        self.SCRN_registeradminacc = RegisterAdminAcc_Screen(self.MAIN_WIDGET)
        self.SCRN_viewproperty = ViewProperty_Screen(self.MAIN_WIDGET)
        self.SCRN_addproperty = AddProperty_Screen(self.MAIN_WIDGET, None)
        self.SCRN_searchfilter = SearchFilter_Screen(self.MAIN_WIDGET)
        self.SCRN_generaldashboard = GeneralDashboard_Screen(self.MAIN_WIDGET, None)
        
        # - Adding it to the stack will be sorted by index number 
        self.MAIN_WIDGET.addWidget(self.SCRN_loginacc)         # INDEX 0
        self.MAIN_WIDGET.addWidget(self.SCRN_registeracc)      # INDEX 1
        self.MAIN_WIDGET.addWidget(self.SCRN_verifyacc)        # INDEX 2
        self.MAIN_WIDGET.addWidget(self.SCRN_dashboard)        # INDEX 3 
        self.MAIN_WIDGET.addWidget(self.SCRN_registeradminacc) # INDEX 4
        self.MAIN_WIDGET.addWidget(self.SCRN_viewproperty)     # INDEX 5
        self.MAIN_WIDGET.addWidget(self.SCRN_addproperty)      # INDEX 6
        self.MAIN_WIDGET.addWidget(self.SCRN_searchfilter)     # INDEX 7
        self.MAIN_WIDGET.addWidget(self.SCRN_generaldashboard) # INDEX 8
        
        # - Starting with the first screen being visible
        self.MAIN_WIDGET.setCurrentIndex(0) # Makes the login screen the first visible screen
    #endregion 
#endregion 

#       MAIN FUNCTION 
# - Will contain code for running the main application 
def main():
    app = QApplication(sys.argv)
    window = SomsManagementLoginSystem()
    window.show () 
    sys.exit(app.exec_())

#      RUNNING APPLICATION
if __name__ == "__main__":
    main()
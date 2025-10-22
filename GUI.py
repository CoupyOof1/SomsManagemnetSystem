#region Import List
import sys                                     # Interacting with the system
import random                                  # Making use of random for generating code

#      IMPORTING PYQT5 LIBRARY FOR GUI INTERFACE
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt5.QtCore import Qt
#endregion

class GUIClass(QWidget):
    # - GUI Class will be used to store all functions needed to create the program's GUI compotents
    
    def __init__(self, widget_stack=None):
        super().__init__()               # Intializing the class 
        self.widget_stack = widget_stack # Keep as a references for the QStackWidget

    def Create_Button(self, text, text_size, xpos, ypos, width, height, connected=None):
        button = QPushButton(text, self)                 # Assigning text and button variable
        button.setGeometry(xpos, ypos, width, height)    # Setting up it scale and proportions
        button.setStyleSheet(f"font-size: {text_size};") # Adjusting the text size
        button.clicked.connect(connected)                # Linked with it needed functionality

    def Create_InputField(self, parent_layout, lbl_text, placeholder=""):
        # - Creating a labelled Input Field 
        # - Adding it to the given parent layout
        layout  = QVBoxLayout()                     # Adding QVBoxLayout for the layout variable
        label  = QLabel(lbl_text)                   # Naming the Input Box
        input_FIELD = QLineEdit()                   # Registering QLineEdit Module for user input
        input_FIELD.setPlaceholderText(placeholder) # Text to put inside the box before input
        layout.addWidget(label)                     # Adding the text onto the layout
        layout.addWidget(input_FIELD)               # Adding InputField to the layout
        parent_layout.addLayout(layout)             # Adding layout to the main parent layout

        # - Scaling the size of the input field
        input_FIELD.setFixedWidth(250)  # width (pixels)
        input_FIELD.setFixedHeight(35)  # height (pixel)

        # - Setting the position of the layout and label
        label.setAlignment(Qt.AlignLeft)
        layout.setAlignment(Qt.AlignHCenter)

        return input_FIELD    
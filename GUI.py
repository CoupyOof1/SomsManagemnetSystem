#region Import List
import sys                                     # Interacting with the system
import random                                  # Making use of random for generating code

#      IMPORTING PYQT5 LIBRARY FOR GUI INTERFACE
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QFrame, QPushButton, QLabel, QStackedWidget, QGridLayout, QSizePolicy, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QIcon # To use with images 
#endregion

class GUIClass(QWidget):
    # - GUI Class will be used to store all functions needed to create the program's GUI compotents
    
    def __init__(self, widget_stack=None):
        super().__init__()               # Intializing the class 
        self.widget_stack = widget_stack # Keep as a references for the QStackWidget

    def Switch_Screens(self, NUM):
        # - A function to switch screens to whatever is desired 
        # 0: Login Screen
        # 1: Register Screen
        # 2: Verfication Screen
        
        self.widget_stack.setCurrentIndex(NUM) # Switches screens to the Desired Screen

    def Create_FrameBox(self, parent_layout, width, height, colour="white"):
        # - Creating a styled frame box with a centered layout inside i.
        # - Will be used to adding in widgets 

        #      (CREATING FRAME) 
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {colour};
                border-radius: 15px;
                border: 2px solid #dcdcdc;
            }}
        """)

        # - Giving the Frame its scale and sizes
        frame.setFixedWidth(width)
        frame.setFixedHeight(height)

        #      (CREATING INNER LAYOUT)
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignCenter)
        frame_layout.setSpacing(15)
        frame.setLayout(frame_layout)

        #      (ADDING FRAME)
        parent_layout.addWidget(frame, alignment=Qt.AlignCenter)

        return frame, frame_layout # Returning both the frame and its inner layout

    def Create_Button(self, text, text_size, parent_layout, connected=None, bg_color="#506a85", text_color="white", hover_color="#2980b9", border_radius=10, btn_align=Qt.AlignHCenter, width=250, height=40, icon_path=None):
        button = QPushButton(text)                                       # Creates a new QPushButton widget with the given text on it 
        #button.setStyleSheet(f"font-size: {text_size}; padding: 8px;")  # Uses the style sheet for styling the button text and padding 
        button.setFixedWidth(width)                                      # Fixes the button width in pixels
        button.setFixedHeight(height)                                    # Fixes the button height in pixels

        #      (CUSTOMISATION)
        button.setStyleSheet(f"""
                QPushButton {{
                    font-size: {text_size};  
                    color: {text_color};
                    background-color: {bg_color};
                    border: none;
                    border-radius: {border_radius}px;
                    padding: 8px 16px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                }}
                QPushButton:pressed {{
                    background-color: #1f5f87;
                }}
        """)

        #      (ADDING ICONS)
        # - Optional, but if the button wants an icon just attach the diretory to that image
        if icon_path != None:
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(64, 64))

        if connected:                         # Checls if a callback function was passed in connected
            button.clicked.connect(connected) # Linked with it needed functionality

        parent_layout.addWidget(button, alignment=btn_align) # Adds the button to the layout and registering it positioning 
        return button                                              # Returns the button widget object for referencing 
    
    def Create_Image(self, image_path, parent=None, width=None, height=None, alignment=Qt.AlignCenter):
        # - This function will create an image for whatever screen

        #      (CREATING IMAGE LABEL)
        image_lbl = QLabel(parent or self) # If parent is not given, attaches to the current widget

        #      (LOADING IMAGE FILE)
        pixmap = QPixmap(image_path)

        # if image is not found or incorrect
        if pixmap.isNull():
            print(f"Image not found at {image_path}") # Print out a warning on console 
            return image_lbl                          # Retruning the empty label if fails to load

        # Resizing if width and height are given
        if width and height: 
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_lbl.setFixedSize(width, height)
        else: 
            image_lbl.setPixmap(pixmap)

        #      (APPLYING PIXMAP AND SCALING)
        # - Applying the pixmap and scaling proportions
        image_lbl.setPixmap(pixmap)
        image_lbl.setScaledContents(True)

        #      (ALIGNING LAYOUTS)
        image_lbl.setAlignment(alignment)

        return image_lbl

    def Create_InputField(self, parent_layout, lbl_text, addtext, placeholder=""):
        # - Creating a labelled Input Field 
        # - Adding it to the given parent layout
        layout  = QVBoxLayout()                     # Adding QVBoxLayout for the layout variable
        label  = QLabel(lbl_text)                   # Naming the Input Box
        input_FIELD = QLineEdit()                   # Registering QLineEdit Module for user input
        input_FIELD.setPlaceholderText(placeholder) # Text to put inside the box before input
        layout.addWidget(input_FIELD)               # Adding InputField to the layout
        parent_layout.addLayout(layout)             # Adding layout to the main parent layout

        # - Scaling the size of the input field
        input_FIELD.setFixedWidth(250)  # width (pixels)
        input_FIELD.setFixedHeight(35)  # height (pixel)

        if addtext == True:
            layout.addWidget(label)          # Adding the text onto the layout
            label.setAlignment(Qt.AlignLeft) # Setting the position of the layout and label
        else:
            pass

        layout.setAlignment(Qt.AlignHCenter) # Setting the position of the layout

        return input_FIELD

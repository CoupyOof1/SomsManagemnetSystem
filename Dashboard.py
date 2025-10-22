import sys 

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget

class Dashboard_Screen(QWidget):
    def __init__(self, widget_Stack):
        super().__init__()                # Intializing the class 
        self.widget_screen = widget_Stack # Keep as a references for the QStackWidget

        
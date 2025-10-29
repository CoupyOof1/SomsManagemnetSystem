#region Import List
import sys 

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget

#      IMPORTING OTHER FILES IN THE FOLDER
from GUI import * # Creating the GUI interface 
#endregion

#region General Dashboard 
class Dashboard_Screen(GUIClass):
    def __init__(self, widget_Stack):
        super().__init__(widget_Stack) # Intializing the class 
        
        #      (SETUP LAYOUT)
        self.layout = QVBoxLayout() # Creates vertical layout container
        self.setLayout(self.layout) # Assigning layout to main window
        self.layout.setSpacing(0)  

        #      (CREATING BACKGROUND IMAGE)
        self.background_image = self.Create_Image(
            "Assets/Images/Dashboard.png",    # Path to your image
            self,                             # Parent (optional)
            width=760,                        # Optional resize width
            height=590                        # Optional resize height
        )
        self.background_image.move(0, 0) # Place it at (0, 0) to fill the window and stay behind everything
        self.background_image.lower()    # Send it behind other widgets

        #      (CREATING GRID LAYOUT)
        # - Creating the gridlayout for buttons placement 
        menu_Layout = QGridLayout()
        menu_Layout.setSpacing(15)
        menu_Layout.setContentsMargins(30, 30, 30, 30)

        #      (SETUP BUTTON NAMES)
        # - Setting up the button names and their position on the grid for presentation
        BTNS_Names = [
            ("View All Property", (0, 0), "Assets/Images/Icons/IC_BTN_VP.png"), # Button 1
            ("Search Property", (0, 1), "Assets/Images/Icons/IC_BTN_SP.png"),   # Button 2 
            ("Add Property", (1, 0), "Assets/Images/Icons/IC_BTN_VP.png"),      # Button 3
            ("Register Admin", (1, 1), "Assets/Images/Icons/IC_BTN_VP.png"),    # Button 4 
            ("Logout", (2, 0, 1, 2), "Assets/Images/Icons/IC_BTN_VP.png")       # Button 5
        ]

        #     (CREATING BUTTONS)
        # - Creating and adding button
        for name, position, iconname in BTNS_Names: 
            # - Creating a placehold for hosting each button
            # - Each button will be added directly to the layout
            # - controlling placement in the grid 

            container = QVBoxLayout()

            btn = self.Create_Button(
                text=name,
                text_size="20px",
                parent_layout=container,
                connected=lambda _, n=name: self.Button_Test(n),
                bg_color="#2C3E50", 
                hover_color="#34495E",
                border_radius=20, 
                width=300, 
                height=100,
                icon_path=iconname
            )

            #      (FITTING BUTTON)
            # - Making the buttons expand and fill the sapce in the menu layout
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            #      (ADDING CONTAINER)
            # - Adding the container layout to the grid cell
            menu_Layout.addLayout(container, *position)

        #       (ADDING GRID)
        self.layout.addLayout(menu_Layout)

    def Button_Test(self, name):
        print(name) 
#endregion

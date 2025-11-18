#region Import List
import sys 

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget

#      IMPORTING OTHER FILES IN THE FOLDER
from GUI import * # Creating the GUI interface 
from Property import * 
#endregion

#      EXPLAINATION
"""
    The code down below is for establishing the dashboard for either general
    or admin roles with distinct features. Such as the folllowing;

    (GENERAL)
    - View Properties 
    - Search Properties
    - Log Out 

    (ADMIN)
    - View Properties 
    - Search Properties
    - Log Out 
    - Reports 
    - Register Admin
    - Add Property

    These will be buttons for each dashboard that corresponds with the user
    roles, and leads them to the appropriate screens for each user.
"""

#region General Dashboard 
class GeneralDashboard_Screen(GUIClass):
    def __init__(self, widget_Stack, nameofuser):
        super().__init__(widget_Stack)   # Intializing the class 
        self.user_name = nameofuser      # Name of the user 
        self.SCRN_Current = widget_Stack # Referencing the current screen 

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
        # - Setting up the button names and their position on the grid for presentation and registering its icon
        BTNS_Names = [
            ("View All Property", (0, 0), "Assets/Images/Icons/IC_BTN_VP.png"), # Button 1 | Name/PositionOnGrid/Asset
            ("Search Property", (0, 1), "Assets/Images/Icons/IC_BTN_SP.png"),   # Button 2 | Name/PositionOnGrid/Asset
            ("Logout", (1, 0), "Assets/Images/Icons/IC_BTN_VP.png")       # Button 5 | Name/PositionOnGrid/Asset
        ]

        #     (CREATING BUTTONS)
        # - Using a loop to create and assign each button to the respected axis on the grid 
        for name, position, iconname in BTNS_Names: 
            # - Creating a placehold for hosting each button
            # - Each button will be added directly to the layout
            # - controlling placement in the grid 

            container = QVBoxLayout()

            btn = self.Create_Button(
                text=name,
                text_size="20px",
                parent_layout=container,
                connected=lambda _, n=name: self.FUNC_BTN_ACTIVE(n),
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

    def FUNC_BTN_ACTIVE(self, name):
        # - A function to allow all the buttons to be pressed and inherit from to execute different actions
        print(name) 

        #      (STORING PREVIOUS SCREEN)
        # - Storing the previous screen before switching
        self.Set_PreviousScreen(self.SCRN_Current)

        # - Creating a dictionary that maps menu options names as strings 
        # - Registerign each action name with an index number
        BTN_Action = {
            "Logout": 0,            # Goes to the Login Screen
            "View All Property": 5, # Goes to the View Property Screen
            "Search Property": 7,
        }

        #      (CHECKING NAME AND ACTIONS)
        # - Checks if the selected name exist within the dictionary 
        if name in BTN_Action: 
            self.widget_stack.setCurrentIndex(BTN_Action[name]) # Gets the corresponding index from dictionary and switches to that screen
            print(self.user_name)
        else:
            print(f"Uknown Screen Option: {name}") # If it doesnt exist it prints a terminal message
#endregion
#region Admin Dashboard 
class AdminDashboard_Screen(GUIClass):
    def __init__(self, widget_Stack, nameofuser):
        super().__init__(widget_Stack) # Intializing the class 
        self.user_name = nameofuser    # Name of the user 

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
        # - Setting up the button names and their position on the grid for presentation and registering its icon
        BTNS_Names = [
            ("View All Property", (0, 0), "Assets/Images/Icons/IC_BTN_VP.png"), # Button 1 | Name/PositionOnGrid/Asset
            ("Search Property", (0, 1), "Assets/Images/Icons/IC_BTN_SP.png"),   # Button 2 | Name/PositionOnGrid/Asset
            ("Add Property", (1, 0), "Assets/Images/Icons/IC_BTN_VP.png"),      # Button 3 | Name/PositionOnGrid/Asset
            ("Register Admin", (1, 1), "Assets/Images/Icons/IC_BTN_VP.png"),    # Button 4 | Name/PositionOnGrid/Asset
            ("Logout", (2, 0, 1, 2), "Assets/Images/Icons/IC_BTN_VP.png")       # Button 5 | Name/PositionOnGrid/Asset
        ]

        #     (CREATING BUTTONS)
        # - Using a loop to create and assign each button to the respected axis on the grid 
        for name, position, iconname in BTNS_Names: 
            # - Creating a placehold for hosting each button
            # - Each button will be added directly to the layout
            # - controlling placement in the grid 

            container = QVBoxLayout()

            btn = self.Create_Button(
                text=name,
                text_size="20px",
                parent_layout=container,
                connected=lambda _, n=name: self.FUNC_BTN_ACTIVE(n),
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

    def FUNC_BTN_ACTIVE(self, name):
        # - A function to allow all the buttons to be pressed and inherit from to execute different actions
        print(name) 

        # - Creating a dictionary that maps menu options names as strings 
        # - Registerign each action name with an index number
        BTN_Action = {
            "Logout": 0,            # Goes to the Login Screen
            "Register Admin": 4,    # Goes to the register admin screen
            "View All Property": 5, # Goes to the View Property Screen
            "Add Property": 6,
            "Search Property": 7,
        }

        #      (CHECKING NAME AND ACTIONS)
        # - Checks if the selected name exist within the dictionary 
        if name == "Add Property":
            #      [CREATING ADD PROPERTY SCREEN PASSING DATA]
            # - Creating the add property screen and passing user's name
            scrn_addprop = AddProperty_Screen(self.widget_stack, nameofUser=self.user_name)
            self.widget_stack.addWidget(scrn_addprop)
            self.widget_stack.setCurrentWidget(scrn_addprop)
        if name in BTN_Action: 
            self.widget_stack.setCurrentIndex(BTN_Action[name]) # Gets the corresponding index from dictionary and switches to that screen
            print(self.user_name)
        else:
            print(f"Uknown Screen Option: {name}") # If it doesnt exist it prints a terminal message
#endregion

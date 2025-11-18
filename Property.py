#region Import List
import sys 
import csv, os
import shutil                 # For copying source file of a directory 
from datetime import datetime # Retrieviing info regarding the current date

#      IMPORTING OTHER FILES IN THE FOLDER
from GUI import * # Creating the GUI interface 
#endregion

#region View Property Screen
class ViewProperty_Screen(GUIClass):
    def __init__(self, widget_stack=None):
        super().__init__(widget_stack) # Intialising the class 

        #      (PATH TO CSV)
        # - Determining the path of the property database CSV File
        self.csv_path = "Assets/Files/PropertyData.csv"  # Directory to the csv file
        self.image_Directory = "Assets/Images/Property/" # Folder for where the property images are stored

        #      (CREATING BACKGROUND IMAGE)
        self.background_image = self.Create_Image(
            "Assets/Images/Background.png",    # Path to your image
            self,                              # Parent (optional)
            width=760,                         # Optional resize width
            height=590                         # Optional resize height
        )
        self.background_image.move(0, 0) # Place it at (0, 0) to fill the window and stay behind everything
        self.background_image.lower()    # Send it behind other widgets

        #      (CREATING VERTICAL LAYOUT)
        # - Creating the base vertical layout for the screen
        layout = QVBoxLayout(self)       # Creating the base vertical layout
        layout.setAlignment(Qt.AlignTop) # Setting it alignment 

        #      (CREATING BACK BUTTON)
        self.Create_Button(
            text="BACK",
            text_size="14px",
            parent_layout=layout,
            connected=self.Switch_BackScreen,
            bg_color="#2C3E50",
            hover_color="#34495E",
            width=150,
            height=40
        )

        #      (ADDING A SCROLLING AREA)
        # - Adding a scrolling area to be able to scroll through all properties details
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        #       (CREATING A WIDGET FOR HOLDING PROPERTY)
        # - Creating a vertical layout for the scrollable content 
        self.scroll_content = QWidget()
        scroll_area.setWidget(self.scroll_content)

        #       (CREATING VERTICAL LAUOUT FOR CONTENT)
        # - Creating a vertical layout just for the scrollable content 
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        #       (LOAD/DISPLAY ALL PROPERTIES INFO)
        # - Displaying and loading all properties information from the csv
        self.load_all_properties()

    def load_all_properties(self):
        # - Reading the CSV file and creating visual cards for each property

        #     (OPENING THE CSV)
        # - Opening the csv file in read mode
        try:
            with open(self.csv_path, newline='', encoding='cp1252') as file:
                reader = csv.DictReader(file) # Reads each row as a dictionary

                #     [LOOPS EACH PROPERTY]
                # - Loops through each property in each row
                for row in reader:

                    #     <CREATES FRAME>
                    # - Creates a frame for each property card
                    frame, frame_layout = self.Create_FrameBox(
                        parent_layout=self.scroll_layout,
                        width=550,
                        height=400,
                        colour="#f8f9fa"
                    )

                    #     <PROPERTY IMAGE>
                    filename_img = f"{row['Name']}.png"
                    path_img = os.path.join(self.image_Directory, filename_img)

                    #     <CREATING IMAGE> 
                    lbl_img = self.Create_Image(
                        image_path=path_img,
                        parent=frame,
                        width=700,
                        height=450
                    )

                    #     <PROPERTY TITLE>
                    lbl_title = QLabel(f"{row['Name']} - {row['Type']}")
                    lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50")
                    frame_layout.addWidget(lbl_title, alignment=Qt.AlignCenter)

                    #     <PROPERTY DETAILS>
                    txt_details = (
                        f"<b>Floors:</b> {row['Floors']}  |  "
                        f"<b>Area:</b> {row['Square Meterage']} sqm  |  "
                        f"<b>Parking:</b> {row['Parking']}<br>"
                        f"<b>Availability:</b> {row['Availability']}  |  "
                        f"<b>Cost:</b> {row['Cost']}<br>"
                        f"<b>Status:</b> {row['Status']}<br>"
                        f"<b>Address:</b> {row['Address']}, {row['City']}, {row['Postcode']}<br>"
                        f"<b>Added:</b> {row['Date']} by {row['Added By']}"
                    )
                    lbl_details = QLabel(txt_details)
                    lbl_details.setWordWrap(True)
                    lbl_details.setStyleSheet("font-size: 13px; color: #555; margin-top: 5px;")
                    frame_layout.addWidget(lbl_details)

                    #     <PROPERTY DESCRIPTION>
                    lbl_desc = QLabel(f"<b>Description:</b><br>{row['Description']}")
                    lbl_desc.setWordWrap(True)
                    lbl_desc.setStyleSheet("font-size: 13px; color: #333; margin: 10px 0;")
                    frame_layout.addWidget(lbl_desc)

                    #     <ADDING VIEW MORE BUTTON>
                    self.Create_Button(
                        text="View Details",
                        text_size="14px",
                        parent_layout=frame_layout,
                        width=200,
                        height=35, 
                        bg_color="#506a85",
                        hover_color="#2980b9",
                        connected=lambda _,r=row: self.open_property_view(r['Name'])
                        )
                    
                    # Adding spaces between each property card
                    self.scroll_layout.addSpacing(15)
                
        except FileNotFoundError:
            self.scroll_layout.addWidget(QLabel("Property data file not found."))

    def open_property_view(self, property_name):
        # - This will be a function for openign property view screen for the selected property
        
        #      (STORING PREVIOUS SCREEN)
        # - Storing the previous screen before switching
        #self.Set_PreviousScreen()

        #      (CREATING NEW DETAILED PROPERTY SCREEN)
        # - Creting new detailed property screen and passing the property name
        scrn_details = DetailProperty_Screen(self.widget_stack, property_name=property_name)

        #      (ADDING THE SCREEN TO THE STACKED WIDGET)
        self.widget_stack.addWidget(scrn_details) # Switches to the detailed property screen

        #      (SHOWING IT)
        self.widget_stack.setCurrentWidget(scrn_details)
#endregion

#region Detail Property Screen
class DetailProperty_Screen(GUIClass):
    def __init__(self, widget_stack=None, property_name=None):
        super().__init__(widget_stack)     # Intialising the class
        self.property_name = property_name # Extracting the name of the property

        #     (PATH TO THE CSV FILE + IMAGE FOLDER)
        self.csv_path = "Assets/Files/PropertyData.csv"
        self.image_path = "Assets/Images/Property/"

        #      (SETUP LAYOUT)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        #      (SCROLLABLE AREA)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        #      (INNER SCROLLABLE CONTENT)
        self.wdget_content = QWidget()
        scroll_area.setWidget(self.wdget_content)

        #      (LAYOUT FOR THE CONTENT)
        self.content_layout = QVBoxLayout(self.wdget_content)
        self.content_layout.setAlignment(Qt.AlignTop)

        #      (LOAD/SHOWING PROPERTY DETAILS)
        self.display_property_details() 
    
    def display_property_details(self):
        # - This will be a function that reads and displays the csv details for the selected property

        #     (READING THE CSV FILE)
        try:
            with open(self.csv_path, newline='', encoding='cp1252') as file:
                reader = csv.DictReader(file)

                #      [LOOPS THROUGH ALL ROWS]
                # - Will go through all rows until correct property is located
                for row in reader: 
                    if row["Name"].strip().lower() == self.property_name.strip().lower():
                        self.build_property_ui(row) # Displays the row information
                        return                      # Stops reading further
                    
            self.content_layout.addWidget(QLabel("Property not found."))

        except FileNotFoundError:
            self.content_layout.addWidget(QLabel("Property data file not found"))

    def build_property_ui(self, data):
        # - Builds the visual layout for the detailed view 

        #      (PROPERTY IMAGE)
        filename_image = f"{data['Name']}.png"
        path_image = os.path.join(self.image_path, filename_image)

        #      (CREATING IMAGE)
        img = self.Create_Image(
            image_path=path_image,
            parent=self.wdget_content,
            width=600,
            height=350
        )
        self.content_layout.addWidget(img, alignment=Qt.AlignCenter)

        #      (PROPERTY TITLE)
        lbl_title = QLabel(f"{data['Name']} — {data['Type']}")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin: 10px 0;")
        lbl_title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(lbl_title)

        #      (PROPERTY DETAILS)
        lbl_details = QLabel(
            f"<b>Floors:</b> {data['Floors']}<br>"
            f"<b>Area:</b> {data['Square Meterage']} sqm<br>"
            f"<b>Parking:</b> {data['Parking']}<br>"
            f"<b>Availability:</b> {data['Availability']}<br>"
            f"<b>Cost:</b> {data['Cost']}<br>"
            f"<b>Status:</b> {data['Status']}<br>"
            f"<b>Address:</b> {data['Address']}, {data['City']}, {data['Postcode']}<br>"
            f"<b>Date Added:</b> {data['Date']}<br>"
            f"<b>Added By:</b> {data['Added By']}"
        )
        lbl_details.setWordWrap(True)
        lbl_details.setStyleSheet("font-size: 14px; color: #444; margin: 10px 25px;")
        self.content_layout.addWidget(lbl_details)

        #      (PROPERTY DESCRIPTION)
        lbl_desc = QLabel(f"<b>Description:</b><br>{data['Description']}")
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("font-size: 14px; color: #333; margin: 10px 25px;")
        self.content_layout.addWidget(lbl_desc)

        #      (BACK BUTTON)
        self.Create_Button(
            text="Back to Property List",
            text_size="16px",
            parent_layout=self.content_layout,
            connected=lambda: self.Switch_Screens(5),  # go back to list
            bg_color="#34495e",
            hover_color="#2c3e50",
            width=250,
            height=45
        )
#endregion

#region Add Property Screen
class AddProperty_Screen(GUIClass):
    def __init__(self, widget_stack=None, nameofUser=None):
        super().__init__(widget_stack) # Intializing the class 
        self.user_name = nameofUser    # Storing the username
        self.img_path_prop = None      # Stores the path of selected image

        #      (SETUP LAYOUT)
        self.layout = QVBoxLayout() # Creating vertical layout container 
        self.setLayout(self.layout) # Assigning the layout to the main window

        #      (CREATING BACKGROUND IMAGE)
        self.background_image = self.Create_Image(
            "Assets/Images/Background.png",    # Path to your image
            self,                              # Parent (optional)
            width=760,                         # Optional resize width
            height=590                         # Optional resize height
        )
        self.background_image.move(0, 0) # Place it at (0, 0) to fill the window and stay behind everything
        self.background_image.lower()    # Send it behind other widgets

        #      (SETUP WHITE BOX FRAME)
        # - Creating a white box for storing the buttons and input fields 
        self.frame, frame_layout = self.Create_FrameBox(self.layout, 340, 560)

        #      (CREATING PROPERTY DETAILS INPUT FIELDS)
        self.ENTName_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Building Name"
        )
        self.ENTType_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Type (eg. Warehouse, Store, Office, etc)"
        )
        self.ENTFloor_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Floor (eg. 1-4)"
        )
        self.ENTSquareMet_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Square Meterage"
        )
        self.ENTParking_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Parking Amount"
        )
        self.ENTAvailability_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Availability (eg. Lease, Purchase, Both)"
        )
        self.ENTCost_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Cost Amount"
        )
        self.ENTAddress_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Address"
        )
        self.ENTCity_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter City"
        )
        self.ENTPostcode_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Postcode"
        )
        self.ENTDescription_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Description"
        )
        self.ENTStatus_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Status"
        )

        #      (CREATING UPLOAD IMAGE BUTTON)
        self.BTN_UploadPropImg = self.Create_Button(
            "Upload Property Image",
            "16px",
            frame_layout,
            self.FuncUpload_Image,
            btn_align=Qt.AlignHCenter,
            width=250,
            height=30,
            icon_path=None
        )

        #      (LABEL FOR SELECTED IMAGE)
        # - Creating a label that showcase if the selected image has been determined
        self.lbl_img_select = QLabel("No Image Selected")
        self.lbl_img_select.setStyleSheet("font-size: 12px; color: gray; margin-bottom: 10px;")
        frame_layout.addWidget(self.lbl_img_select, alignment=Qt.AlignHCenter)

        #      (CREATING PROPERTY BUTTON)
        self.BTN_CreateProperty = self.Create_Button(
            "Submit", 
            "18px", 
            frame_layout, 
            self.FunCreate_Property, 
            btn_align=Qt.AlignHCenter,
            width=250,
            height=30,
            icon_path=None
        )
    
    def FunCreate_Property(self):
        # - This will be a function that overwrites and add new property details to the csv file

        #      (RETRIEVING INPUT VALUES)
        # - Retrieving the credentials of the property from the following input fields
        name_PROP = self.ENTName_InputField.text().strip()
        type_PROP = self.ENTType_InputField.text().strip()
        floor_PROP = self.ENTFloor_InputField.text().strip()
        sqmet_PROP = self.ENTSquareMet_InputField.text().strip()
        park_PROP = self.ENTParking_InputField.text().strip()
        avail_PROP = self.ENTAvailability_InputField.text().strip()
        cost_PROP = self.ENTCost_InputField.text().strip()
        adrs_PROP = self.ENTAddress_InputField.text().strip()
        city_PROP = self.ENTCity_InputField.text().strip()
        posde_PROP = self.ENTPostcode_InputField.text().strip()
        desc_PROP = self.ENTDescription_InputField.text().strip()
        sttus_PROP = self.ENTStatus_InputField.text().strip()

        csv_path = "Assets/Files/PropertyData.csv"         # Path to the CSV File
        date_created = datetime.now().strftime("%d/%m/%Y") # Retrieving the current date 

        #      (VALIDATION)
        # - Ensuring the User has inputed the following needed info
        if not name_PROP:
            print("Please enter a property name.")
            return 

        #      (CHECKING FOR DUPLICATION)
        # - Checking if the name of the property alread exist for avoiding duplication
        try:
            with open(csv_path, mode="r", encoding="cp1252") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row = {k.strip(): v for k, v in row.items()} 
                    if row["Name"].strip().lower() == name_PROP.lower():
                        print("An property with this name exist")
                        return
        except FileNotFoundError:
            pass 
        
        #     (SAVING IMAGE)
        # - Copying the image and renaming it to match the property name for it new path
        try: 
            folder_path = "Assets/Images/Property/" # Path to save the image to 
            os.makedirs(folder_path, exist_ok=True)
            dest_path = os.path.join(folder_path, f"{name_PROP}.png")
            shutil.copyfile(self.img_path_prop, dest_path)
            print(f"Image saved as {dest_path}")
        except Exception as e:
            print(f"Error saving image {e}")
        
        #     (APPENDING NEW PROPERTY DETAILS ON CSV FILE)
        # - Adding those new property detzails onto the csv file
        try: 
            with open(csv_path, mode="a", newline="", encoding="cp1252") as file:
                writer = csv.writer(file)
                writer.writerow([name_PROP, type_PROP, floor_PROP, sqmet_PROP, park_PROP, avail_PROP, cost_PROP, adrs_PROP, city_PROP, posde_PROP, desc_PROP, sttus_PROP, date_created, self.user_name])  
                self.Switch_Screens(5),  # go back to list
        except Exception as e:
            print(f"Error saving property details: {e}")
            return 
        
    def FuncUpload_Image(self):
        # - This will be a function that allows users to upload their image to be the preview of the property

        #      (ESTABLISHING VARIABLE)
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Property Image",
            "",
            "Image File (* .png)"
        ) 
        if file_path:
            self.img_path_prop = file_path
            filename = os.path.basename(file_path)
            self.lbl_img_select.setText(f"Selected: {filename}")

#endregion
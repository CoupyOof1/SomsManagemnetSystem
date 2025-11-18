#region Import List
import sys 
import csv, os
#      IMPORTING OTHER FILES IN THE FOLDER
from GUI import *                        # Creating the GUI interface 
from Property import ViewProperty_Screen # Showcasing property details 
#endregion

#      EXPLAINATION 
"""
    Code down below will be for searching and filtering
    properties in accords to the user's preferences.
    Allowing users to filter by specific categories and 
    output their most likely desired result.
    
    Along with searches, it also saves the outputted 
    result asa a report.
"""

class SearchFilter_Screen(GUIClass):
    def __init__(self, widget_stack=None):
        super().__init__(widget_stack)                              # Intializing the class 
        self.viewpropertyscreen = ViewProperty_Screen(widget_stack) # Referencing the view property screen

        #      (SETUP LAYOUT)
        self.layout = QHBoxLayout() # Creates Horizontal layout container
        self.setLayout(self.layout) # Assigning layout to main window
        self.layout.setSpacing(10)

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
        # - Creating a White box to store the buttons, and input fields
        self.frame, frame_layout = self.Create_FrameBox(self.layout, 340, 380, Qt.AlignLeft)

        #      (CREATING SEARCH BAR)
        # - Creating the search bar to allow users to search for specific properties
        self.Search_Bar = self.Create_InputField(
            frame_layout, 
            "",
            False,
            "Search"
        )

        #      (CREATING SEARCH FILTERS)
        self.filter_PName = self.Create_InputField(
            frame_layout,
            "Name",
            True,
            "Enter property name"
        )
        self.filter_PType = self.Create_InputField(
            frame_layout,
            "Type",
            True,
            "E.g: Office, Warehouse, Store..."
        )
        self.filter_PAvail = self.Create_InputField(
            frame_layout,
            "Availability",
            True,
            "E.g: Lease, Purchase..."
        )
        self.filter_PCity = self.Create_InputField(
            frame_layout,
            "City",
            True,
            "Enter city name"
        )
        self.filter_PStatus = self.Create_InputField(
            frame_layout,
            "Status",
            True,
            "E.g: Available, Leased, Sold"
        )

        #      (SETUP DROPDOWN LSIT)
        # - Creating a dropdwon list by using the QListWidget modules, creating a whole new windwo for displaying results
        self.bar_search_list = QListWidget()                  # Associoating the variable with the QListWidget          
        self.bar_search_list.hide()                           # Hiding the list by default, it will only be shown when typing into search bar
        self.bar_search_list.setWindowTitle("Search Results") # Naming the window that will display the search results

        #      (LOADING DATASET FROM CSV FILE)
        # - Using the try+except method for loading specific datasets 
        # - In any case it fails to capture it, the program will continue to run without issue.
        try:
            with open("Assets/Files/PropertyData.csv", "r", encoding="cp1252") as file: 
                #      [READING/EXTRACTING DATA]
                # - Reading and extractng the data from each line in the  csv 
                reader = csv.DictReader(file)
                self.data = [row for row in reader] # Extracts Data 
        except FileNotFoundError:
            print("Data not found search results") # Debugging and logging 

        #      (FORMING CONNECTIONS TO THE PROPER FUNCTION)
        # - Connects the bar search/list towards the corresponding function for correct action execution
        self.Search_Bar.textChanged.connect(self.update_list)
        self.bar_search_list.itemClicked.connect(self.select_item)

        #      [CONNECTING FILTERS TO FUNCTION]
        # - Connecting the filter inputs to the update list function
        self.filter_PName.textChanged.connect(self.update_list)
        self.filter_PType.textChanged.connect(self.update_list)
        self.filter_PAvail.textChanged.connect(self.update_list)
        self.filter_PCity.textChanged.connect(self.update_list)
        self.filter_PStatus.textChanged.connect(self.update_list)

        #      (ADDING SCROLLING AREA)
        # - Adding a scrolling area to scroll search results of the property 
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)

        #      (CREATING WIDGET FOR HOLDING PROPERTY)
        # - Creates a vertical layout for the scrollable content 
        self.scroll_content = QWidget()
        scroll_area.setWidget(self.scroll_content)

        #      (CREATING VERTICAL LAYOUT OF CONTENT)
        # - Creates vertical layout for the scrollable content
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignRight)

    def update_list(self, text):
        # - This will be a function used for updating the results fron the dropdown list 

        self.bar_search_list.clear() # Clears the content of the results first before input
        PROP_NameFLTR = self.filter_PName.text().lower().strip()
        PROP_TypeFLTR = self.filter_PType.text().lower().strip()
        PROP_AvailFLTR = self.filter_PAvail.text().lower().strip()
        PROP_CityFLTR = self.filter_PCity.text().lower().strip()
        PROP_StatusFLTR = self.filter_PStatus.text().lower().strip()

        #      (HIDING RESULT LIST)
        # - If there no text in the search bar the result will be hidden
        if not text:
            self.bar_search_list.hide() # Hiding the listed results 
            return                      # Returns the origram so it can continue 
        
        text = text.lower() # Making search case-insenetive 

        #      (FILTER RESULTS)
        # - Matching each r esults if the search terms appear in any of the columns in the dataset
        results = []          # Creating an eptu list that will store rows from the CSV file
        for row in self.data: # Looping through every row in the CSV File 
            
            match = False                          # Indication for not appending results in list yet 
            if text:                               # If the main search bar has text 
                for value in row.values():         # Gives all the values from the dictionary
                    if text in str(value).lower(): # Converts each filed value to a string and lowercase
                        match = True               # Turn it to true so it can be appened to the following columns
                        break                      # Found a match in the row and skips the remaining fields 
                    else:
                        match = True               # Turn it to true so it can be appened to the following columns
            #      [PROPERTY NAME FILTER]
            if self.filter_PName:
                if PROP_NameFLTR not in row["Name"].lower():
                    match = False
            #      [PROPERTY TYPE FILTER]
            if self.filter_PType:
                if PROP_TypeFLTR not in row["Type"].lower():
                    match = False
            #      [PROPERTY AVAILABILITY FILTER]
            if self.filter_PAvail:
                if PROP_AvailFLTR not in row["Availability"].lower():
                    match = False
            #      [PROPERTY CITY FILTER]
            if self.filter_PCity:
                if PROP_CityFLTR not in row["City"].lower():
                    match = False
            #      [PROPERTY STATUS FILTER]
            if self.filter_PStatus:
                if PROP_StatusFLTR not in row["Status"].lower():
                    match = False
            if match: 
                results.append(row) # the columns value the entire row dictionary is added

        #      (NO RESULTS FROM FILTERED INPUT)
        # - If no results from filtered input it will show the list 
        for result in results:          
            name = result.get("Name", "Unknown")        # Extract the name of the resulted input
            QListWidgetItem(name, self.bar_search_list) # Showcasing the result based on user's input

        #      (CREATING DYNAMIC HEIGHT FOR RESULT LIST)
        # - Creating dynamic height adjustmnet based on the quantity of the result after filter
        row_height = 30  # Baseline estimation of how tall each row is 
        max_height = 200 # Cap Height to ensure it doesnt exceed in growth
        srchbar_ht_adjust = min(len(results) * row_height, max_height)

        #      (SETUP DROPDOWN POSITION)
        # - Positioning the dropdown diretly under the search bar 
        self.bar_search_list.setGeometry(                   # Setting the actual positioning and width of the results
            self.Search_Bar.x(),                            # Registering its X position the same as the searchbar's
            self.Search_Bar.y() + self.Search_Bar.height(), # Registering its Y position to be Search bar's Y + its height  to be placed under   
            self.Search_Bar.width(),                        # Registering it width to be the same as the search bar 
            srchbar_ht_adjust                               # Registering it height to be the adjust height variable for dynamic adjustment 
        )

        # Showcasing the results list  
        self.bar_search_list.show() 

    def select_item(self, item):
        # - When user clicks on the follow results it will fill the searc h
        propertydata = item.text()
        self.Search_Bar.setText(propertydata)
        self.bar_search_list.hide()

        #      (FILTER THE DATASET)
        # - Filtering the dataset to match the clicked property 
        filter = [row for row in self.data if row.get("Name", "").lower() == propertydata.lower()]

        # - Showcasing the property card in the scroll area 
        if filter:
            self.display_property(filter)

        #     (SAVING RESULT TO REPORT)
        # - Once search is conducted it will save that result on the report csv
        PATH_RPT = "Assets/Files/Report.csv" # Directory towards the file
        PROP_ROW = filter[0]                 # Filtering contains only 1 matching row from search bar
        try:
            with open(PATH_RPT, mode="a", newline="", encoding="cp1252") as file:
                
                #      [RETREIVING DATE/TIME]
                now = datetime.now()
                n_time = now.strftime("%H:%M:%S")
                n_date = now.strftime("%Y-%m-%d")

                #      [CREATE ROW IN ORDER]
                report_rw = [
                    PROP_ROW.get("Name", ""),
                    PROP_ROW.get("Type", ""),
                    PROP_ROW.get("Floors", ""),
                    PROP_ROW.get("Square Meterage", ""),
                    PROP_ROW.get("Availability", ""),
                    PROP_ROW.get("Cost", ""),
                    n_time,
                    n_date
                ]

                #      [WRITING TO THE CSV]
                writer = csv.writer(file)
                writer.writerow(report_rw)
                print("Report saved sucessfully") # Debugging 
        except Exception as e:
            print(f"Error saving report details: {e}")
            return

    def display_property(self, filtereddata):
        # - This will be a function for displaying filtered properties after search 

        #      (CLEARING OLD CARDS)
        # - Clears any old property cards if new search is conducted 
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        #      (LOOPING THROUGH EACH FILTERED PROPERTY)
        # - Loops through each filtered property and creates the card 
        for row in filtereddata:
            # - Creating frame box for each property
            DP_frame, DP_frame_layout = self.Create_FrameBox(
                parent_layout=self.scroll_layout,
                width=550,
                height=400,
                colour="#f8f9fa"
            )

            #      [LOADING PROPERTY IMAGE]
            # - Loading the image for the filtered property 
            filename_img = f"{row['Name']}.png"
            img_path = os.path.join("Assets/Images/Property/", filename_img)
            #      <CREATING IMAGE>
            lbl_img = self.Create_Image(
                image_path=img_path,
                parent=DP_frame,
                width=700,
                height=450
            )

            #      [PROPERTY TITLE]
            # - Showcasing the filtered property title 
            lbl_title = QLabel(f"{row['Name']} - {row['Type']}")
            lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50")
            DP_frame_layout.addWidget(lbl_title, alignment=Qt.AlignCenter)

            #      [PROPERTY DETAILS]
            # - Showcasing the filtered property details 
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
            DP_frame_layout.addWidget(lbl_details)

            #      [PROPERTY DESCRIPTION]
            lbl_desc = QLabel(f"<b>Description:</b><br>{row['Description']}")
            lbl_desc.setWordWrap(True)
            lbl_desc.setStyleSheet("font-size: 13px; color: #333; margin: 10px 0;")
            DP_frame_layout.addWidget(lbl_desc)

            #      [ADDING VIEW MORE BUTTON]
            self.Create_Button(
                text="View Details",
                text_size="14px",
                parent_layout=DP_frame_layout,
                width=200,
                height=35, 
                bg_color="#506a85",
                hover_color="#2980b9",
                connected=lambda _,r=row: self.viewpropertyscreen.open_property_view(r['Name'])
            )
                    
            # Adding spaces between each property card
            self.scroll_layout.addSpacing(15)
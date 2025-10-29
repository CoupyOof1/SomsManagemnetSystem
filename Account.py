#region Import List
import sys                                     # Interacting with the system
import csv                                     # For readign csv 
import smtplib   
from datetime import datetime                  # Retrieving info regarding the date and time
from email.message import EmailMessage
from email.mime.text import MIMEText           # Sending Emails Function
from email.mime.multipart import MIMEMultipart # Importing email module needed
import random                                  # Making use of random for generating code

#      IMPORTING OTHER FILES IN THE FOLDER
from GUI import * # Creating the GUI For Scenes
#endregion

#region Login 
class LoginAcc_Screen(GUIClass):
    def __init__(self, widget_stack):
        super().__init__(widget_stack)    # Intializing the class 

        #      (SETUP LAYOUT)
        self.layout = QVBoxLayout() # Creates vertical layout container
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
        self.frame, frame_layout = self.Create_FrameBox(self.layout, 340, 280)

        #      (SETUP TOP BAR)
        # - Setting up a top bar to place the log in and sign up buttons
        topbar_layout = QVBoxLayout()
        topbar_layout.setAlignment(Qt.AlignTop)
        topbar_layout.setSpacing(10)

        #      (SETUP TITLE)
        title = QLabel("Login to Your Account")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        topbar_layout.addWidget(title, alignment=Qt.AlignCenter)

        frame_layout.addLayout(topbar_layout)

        #      [FULLNAME INPUT FIELD]
        # - Allowing user to input their FullName for loggin in 
        self.FULLNAME_INPUT = self.Create_InputField(
            frame_layout, 
            "",
            False,
            "Email/Fullname"
        )

        #      [PASSWORD INPPUT FI,ELD]
        # - Allowing users to input their password for logging in 
        self.PASSWORD_INPUT = self.Create_InputField(
            frame_layout, 
            "",
            False,
            "Password"
        )

        #      (LOADING DATASETS FROM CSV)
        # - Deploying the try and except method for laoding specific datasets from csv file
        # - In any case it fails to capture any datasets, the program will continue without an error occuring for better handling
        try:
            with open("Assets/Files/UserDatabase.csv", "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)                                          # Creating a csv reader that treats the first row as headers
                self.data = [{k.strip(): v for k, v in row.items()} for row in reader] # Reads all the rows from csv file and clean up the header names
        except FileNotFoundError:
            print("Data not found, Login not useable") # Debugging 
            self.data = []

        #      (SETUP LOGIN BUTTON)
        # - Setting up the login button so once credentials are put in it validates the credentials
        self.BTN_login = self.Create_Button(
            "LOGIN", 
            "18px", 
            frame_layout, 
            self.Check_Credentials, 
            btn_align=Qt.AlignHCenter,
            width=250,
            height=40,
            icon_path=None
        )

        #      (SETUP REGISTER BUTTON)
        # - Setting up the Sign up button to allow users to the sign up page 
        self.BTN_SignUp = self.Create_Button(
            "New to SomsMang? Register for an account", 
            "11px", 
            frame_layout, 
            self.Switch_SignUpScreen, 
            btn_align=Qt.AlignHCenter,
            width=245,
            height=30,
            icon_path=None
        )

        # Attach the frame layout to the frame
        self.frame.setLayout(frame_layout)

        # Add the frame to the main layout (this is the missing line!)
        self.layout.addWidget(self.frame, alignment=Qt.AlignCenter)

    def Switch_SignUpScreen(self):
        self.widget_stack.setCurrentIndex(1) # Switches screens to the Desired Screen
    
    def Check_Credentials(self):
        # - Once users have entered their credentials, it will then be checked upon a press of a button 
        
        #      (EXTRACTING USER INPUT)
        # - Extracting user input to see if it matches with any credentials stored in the dataset
        NAME_INPUT = self.FULLNAME_INPUT.text().lower().strip()     # Converting it to lowercase and remove any leading/trailing spaces.
        PASSWORD_INPUT = self.PASSWORD_INPUT.text().lower().strip() # Converting it to lowercase and remove any leading/trailing spaces.

        #      (PREVENT LOGIN)
        # - This code will be used incase there invalid login or no credentials to ensure they don't get through
        if not NAME_INPUT or not PASSWORD_INPUT:
            print("Please enter both email/fullname and password")
            return 

        #      (CHECKING CREDENTIALS)
        # - Checking if the input credentials matches the one in the dataset 
        if not self.data:                   # If the data list loaded fromn the csv file is empty
            print("No user data available") # Prints a message 
            return                          # Exit the function early since it cant check anything
        
        found_match = False                 # Used for tracking if a matching user was found

        for row in self.data:               # Looping through every row in the dataset
            fullnamedata = row.get("Fullname", "").lower().strip() # Extracting the fullname column from the row and converting it to lowercase and removing space to match
            emaildata = row.get("Email", "").lower().strip()       # Extracting the email column from the row and converting it to the lowercase and removign spaces to match
            passworddata = row.get("Password", "").lower().strip() # Extracting the password column from the row and converting it to lowercase and removing space to match
            
            print(f"DEBUG: Comparing input({NAME_INPUT}, {PASSWORD_INPUT}) "f"with fullname({fullnamedata}), email({emaildata}), password({passworddata})")

            #       [COMPARING USER INPUT WITH CSV DATA]
            if PASSWORD_INPUT == passworddata and (NAME_INPUT == fullnamedata or NAME_INPUT == emaildata):
                found_match = True # If both match found the correct user
                break              # No need to check rows and exit the loop
            
        #      (HANDLING LOGIN/FAILURE ATTEMPTS)
        if found_match:                                                          # If found a match in the csv file execute command
            print("Login Sucessful")                                             # Print sucess message
            verify_Screen = VerifyAcc_Screen(self.widget_stack, emaildata, True) # Passing emaild data to the next screen
            self.widget_stack.setCurrentIndex(2)                                 # Switches screens to the Verification
        else:                            # If no matches were found execute the following command
            print("Invalid Credentials") # Prints invalid credentials message
#endregion

#region Registeration Account 
class RegisterAcc_Screen(GUIClass):
    def __init__(self, widget_Stack):
        super().__init__(widget_Stack) # Intializing the class 

        #      (SETUP LAYOUT)
        self.layout = QVBoxLayout() # Creates vertical layout container
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
        self.frame, frame_layout = self.Create_FrameBox(self.layout, 340, 280)

        #      (CREATING FULLNAME INPUT FIELD)
        self.ENTFullname_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Fullname"
        )

        #      (CREATING EMAIL INPUT FIELD)
        self.ENTEmail_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Email Address"
        )

        #      (CREATING PASSWORD INPUT FIELD)
        self.ENTPassword_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter Password"
        )

        #      (CREATING CONFIRM PASSWORD INPUT FIELD)
        self.ENTConfPassword_InputField = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Confirm Password"
        )

        #     (CREATING ACCOUNT BUTTON)
        self.BTN_CreateAccount = self.Create_Button(
            "Sign Up", 
            "18px", 
            frame_layout, 
            self.Create_Account, 
            btn_align=Qt.AlignHCenter,
            width=250,
            height=40,
            icon_path=None
        )
    def Create_Account(self):
        # - This will be a function where it will overwrite and add new details to the csv user database file

        #      (GETTING INPUT VALUES)
        # - Abstracting credentiasl from the input fields 
        fullname = self.ENTFullname_InputField.text().strip()
        email = self.ENTEmail_InputField.text().strip()
        password = self.ENTPassword_InputField.text().strip()
        confirm_password = self.ENTConfPassword_InputField.text().strip()

        #      (BASIC VALIDATION)
        # - If any of the fields are nto filled in
        if not fullname or not email or not password or not confirm_password:
            print("Please fill in all fields")
            return 
        # - If password doesnt match
        if password != confirm_password:
            print("Password doesn't match")
            return
        
        #     (SETTING ROLE AND DATE)
        # - Setting the role and date of creation of said account
        role = "General"                                   # Assigning user type role
        date_created = datetime.now().strftime("%d/%m/%Y") # Retrieving the current date 
        csv_path = "Assets/Files/UserDatabase.csv"         # Path to the CSV File

        #     (CHECKING FOR DUPLICATION)
        # - Checking if email or name has already exist for avoiding duplication
        try: 
            with open(csv_path, mode="r", encoding="utf-8") as file: 
                reader = csv.DictReader(file)
                for row in reader:                                          # For each row on the csv 
                    row = {k.strip(): v for k, v in row.items()} 
                    if row["Email"].strip().lower() == email.lower():       # On CSV If User with email exist prints message 
                        print("An account with this email exist")           # Printing message on terminal
                        return
                    if row["Fullname"].strip().lower() == fullname.lower(): # On CSV If user with fullname exist prints message
                        print("An account with this name exists")           # Printing message on termianl
                        return
        except FileNotFoundError:
            pass 

        #      (APPENDING NEW USER ON CSV FILE)
        # - Adding those new details onto the csv file 
        try: 
            with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([fullname, role, email, password, date_created]) # Write over the row for the csv with the credentials
                print("Account Created!")                                        # Print message indicating account has been created 
                self.widget_stack.setCurrentIndex(0)                             # Switches screens to the Login Screen
        except Exception as e:
            print(f"Error saving account: {e}")
            return
#endregion

#region Verifying Account https://mailtrap.io/blog/python-send-email/
class VerifyAcc_Screen(GUIClass):
    def __init__(self, widget_Stack, emailofuser, SENDCODE=None):
        super().__init__(widget_Stack)    # Intializing the class 
        self.user_email = emailofuser     # Keep as a references for sending an code 
        self.Generate_Code = SENDCODE

        #      (SETUP LAYOUT)
        self.layout = QVBoxLayout() # Creates vertical layout container
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
        self.frame, frame_layout = self.Create_FrameBox(self.layout, 340, 280)

        #      (SETUP VERICATION CODE)
        # - This will be used for the two step authetnication.
        # - Generating random number of code that will be sent to the user
        if self.Generate_Code == True:
            self.verify_Code = "".join(str(random.randint(1,9)) for _ in range(4))
        else:
            self.verify_Code = "0"

        print(f"{self.verify_Code}")
        print(f"Loaded Verify Screen for: {self.user_email}")

        self.Send_Email() # Sending a email upon reaching this screen 

        #      (CREATING INPUT FIELD)
        self.VerifyCode = self.Create_InputField(
            frame_layout,
            "",
            False,
            "Enter verifcation code"
        )

        #      (CREATING SUBMIT BUTTON)
        self.BTN_login = self.Create_Button(
            "SUBMIT", 
            "18px", 
            frame_layout, 
            self.Check_VerifyCode, 
            btn_align=Qt.AlignHCenter,
            width=250,
            height=40,
            icon_path=None
        )

    def Check_VerifyCode(self):
        # - This will be a function that checks what the user has inputed to see if it matches the verification code

        code = self.verify_Code
        user_input = code.strip() # Extracting what the user typed from the input field

        #      (CHECKING CODE)
        # - Checking if the input field matches the generated code
        if user_input == code:
            print("Verification sucessful! Ascess granted.") # Prints terminal message to indicate acess granted 
            self.widget_stack.setCurrentIndex(3)             # Switches screens to the Dashboard Screen
        else:
            print("Incorrect code, Try Again")

    def Send_Email(self):
        # - This function will send a 4 digit veriication code to the user's email

        #      (CONFIGURING EMAIL)
        email_sender = "somscoupy@gmail.com"           # Your "from" email 
        email_password = "qomqoizcmuxezgze"            # Your Email's App Password
        email_reciever = self.user_email               # The user's email
        email_subject = "SomsManag Verification Code:" # The email's subject
        body = f"Hello, \n\nYour 4-digit verification code is {self.verify_Code}\n\nPlease enter it in the app to enter your account on SomsManagement."

        #      [CREATING EMAIL]
        msg = EmailMessage()
        msg["From"] = email_sender
        msg["To"] = email_reciever
        msg["Subject"] = email_subject

        msg.set_content(body)

        #      [SENDING EMAIL]
        # - Sending email using the Mailtrap SMTP
        try: 
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(email_sender, email_password)
                server.send_message(msg)
                print(f"Email sent to {email_reciever}")

        except Exception as e:
            print(f"Failed to send email {e}")
#endregion
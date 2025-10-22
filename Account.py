#region Import List
import sys                                     # Interacting with the system
import csv                                     # For readign csv 
import smtplib   
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
        #self.widget_screen = widget_Stack # Keep as a references for the QStackWidget

        #      (SETUP LAYOUT)
        self.layout = QVBoxLayout() # Creates vertical layout container
        self.setLayout(self.layout) # Assigning layout to main window
        self.layout.setSpacing(10)

        #      [FULLNAME INPUT FIELD]
        # - Allowing user to input their FullName for loggin in 
        self.FULLNAME_INPUT = self.Create_InputField(
            self.layout, 
            "Email/Fullname",
            "Enter email/fullname"
        )

        #      [PASSWORD INPPUT FI,ELD]
        # - Allowing users to input their password for logging in 
        self.PASSWORD_INPUT = self.Create_InputField(
            self.layout, 
            "Password",
            "Enter password"
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
            "LOGIN", "40px", 380, 525, 100, 100, self.Check_Credentials
        )
    
    def Check_Credentials(self):
        # - Once users have entered their credentials, it will then be checked upon a press of a button 
        
        #      (EXTRACTING USER INPUT)
        # - Extracting user input to see if it matches with any credentials stored in the dataset
        NAME_INPUT = self.FULLNAME_INPUT.text().lower().strip()     # Converting it to lowercase and remove any leading/trailing spaces.
        PASSWORD_INPUT = self.PASSWORD_INPUT.text().lower().strip() # Converting it to lowercase and remove any leading/trailing spaces.

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
        if found_match:                                                    # If found a match in the csv file execute command
            print("Login Sucessful")                                       # Print sucess message
            verify_Screen = VerifyAcc_Screen(self.widget_stack, emaildata) # Passing emaild data to the next screen
            self.widget_stack.setCurrentIndex(2)                           # Switches screens to the Verification
        else:                            # If no matches were found execute the following command
            print("Invalid Credentials") # Prints invalid credentials message
#endregion

#region Registeration Account 
class RegisterAcc_Screen(GUIClass):
    def __init__(self, widget_Stack):
        super().__init__(widget_Stack) # Intializing the class 
#endregion

#region Verifying Account https://mailtrap.io/blog/python-send-email/
class VerifyAcc_Screen(GUIClass):
    def __init__(self, widget_Stack, emailofuser):
        super().__init__(widget_Stack)    # Intializing the class 
        self.user_email = emailofuser     # Keep as a references for sending an code 

        #      (SETUP LAYOUT)
        self.layout = QVBoxLayout() # Creates vertical layout container
        self.setLayout(self.layout) # Assigning layout to main window
        self.layout.setSpacing(10)

        #      (SETUP VERICATION CODE)
        # - This will be used for the two step authetnication.
        # - Generating random number of code that will be sent to the user
        self.VCode1 = random.randint(1,9) # First Digit 
        self.VCode2 = random.randint(1,9) # Second Digit 
        self.VCode3 = random.randint(1,9) # Third Digit 
        self.VCode4 = random.randint(1,9) # Fourth Digit 

        print(f"Loaded Verify Screen for: {self.user_email}")

        self.Send_Email()

        self.VerifyCode = self.Create_InputField(
            self.layout,
            "",
            "Enter verifcation code"
        )

    def Send_Email(self):
        # - This function will send a 4 digit veriication code to the user's email

        #      (COMBINING THE CODE)
        verify_Code = f"{self.VCode1}{self.VCode2}{self.VCode3}{self.VCode4}"

        #      (CONFIGURING EMAIL)
        email_sender = "noreply@example.com"          # Your "from" email 
        email_reciever = self.user_email              # The user's email
        email_subject = "SomsManag Veriication Code:" # The email's subject
        body = f"Hello, \n\nYour 4-digit verification code is {verify_Code}\n\nPlease enter it in the app to verify your account."

        #      [CREATING EMAIL]
        msg = MIMEMultipart()
        msg["From"] = email_sender
        msg["To"] = email_reciever
        msg["Subject"] = email_subject

        msg.attach(MIMEText(body, "plain"))

        #      [SENDING EMAIL]
        # - Sending email using the Mailtrap SMTP
        try: 
            with smtplib.SMTP("sandbox.smtp.mailtrap.io", 587) as server:
                server.starttls()
                server.login(email_sender, "YOUR_MAILTRAP_PASSWORD")
                server.send_message(msg)
                print(f"Email sent to {email_reciever}")

        except Exception as e:
            print(f"Failed to send email {e}")
#endregion
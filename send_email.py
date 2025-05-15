import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(text, user, remitent):
    password = os.environ['EMAIL_PASSWORD']
    username = os.environ['EMAIL']
    emails_to = os.environ['EMAIL_TO']
    email = f'''Mensaje de {user} ({remitent}):
    "{text}"'''
    server = "smtp.gmail.com"
    port = 587
    s = smtplib.SMTP(host=server, port=port)
    s.starttls()
    s.login(username, password)

    msg = MIMEMultipart()  # Creates the message
    msg['To'] = emails_to  # Sets the receiver's email address
    msg['From'] = username  # Sets the sender's email address
    msg['Subject'] = f"Nuevo mensaje en el blog de {user}"  # Sets the subject of the message
    msg.attach(MIMEText(email, 'html'))  # Attaches the email content to the message as html

    s.send_message(msg)  # Sends the message
    del msg  # Deletes the message from memory


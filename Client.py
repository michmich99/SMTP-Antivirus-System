
# Tkinter is a Python library that is used for graphical user interface applications
from tkinter import *
import tkinter as tk
import smtplib
import email.utils
import email.encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

#Main Screen
master = tk.Tk()
master.title('Custom Python Email App')

#Functions

# filling the mail from users input and sending
def send():
    try:
        to = temp_To.get()
        subject = temp_Subject.get()
        body = temp_Body.get()
        fileName = temp_Attachment.get()

        if to=="" or subject=="" or body=="" or fileName=="":
            notifyLabel.config(text='All fields required!', fg="red")
            return
        else:
            # mail will consist of multiple parts - body, attachment
            msg = MIMEMultipart()

            # fill the fields in the mail
            msg['To'] = email.utils.formataddr(('Recipient', to))
            msg['From'] = email.utils.formataddr(('Author', 'author@post.bgu.ac.il'))
            msg['Subject'] = subject

            # attach body as plain text
            msg.attach(MIMEText(body))

            # opening the file that will be sent
            with open(fileName, "rb") as file:

                # defines that the attachment is binary file
                attachment = MIMEBase("application", "octet-stream")
                
                # copy the file content to the mail
                attachment.set_payload(file.read())

            # encode the message's content in Base64 (ASCII characters)
            email.encoders.encode_base64(attachment)

            # add header to the attachment
            attachment.add_header(
                "Content-Disposition",
                f"file; filename= {fileName}",
            )

            # attach the file
            msg.attach(attachment)

            # creates connection to SMTP server
            server = smtplib.SMTP('127.0.0.1', 1025)

            # show communication with the server
            server.set_debuglevel(True)

            # sending the mail
            try:
                server.sendmail('author@post.bgu.ac.il', [to], msg.as_string())
            finally:
                server.quit()

            reset()
            notifyLabel.config(text='Email has been sent', fg="green")
    except:
        notifyLabel.config(text='Error sending email', fg="red")

# reseting the fields in the main screen
def reset():
    toEntry.delete(0, 'end')
    subjectEntry.delete(0, 'end')
    bodyEntry.delete(0, 'end')
    attachmentEntry.delete(0, 'end')

#Graphics
#labels
tk.Label(master, text="Send Email", font=('Calibri', 15)).grid(row=0, sticky=N)
tk.Label(master, text="Fill the form below to send an email", font=('Calibri', 11)).grid(row=1, sticky=W, padx=5)

#fields
tk.Label(master, text="To", font=('Calibri', 11)).grid(row=2, sticky=W, padx=5)
tk.Label(master, text="Subject", font=('Calibri', 11)).grid(row=3, sticky=W, padx=5)
tk.Label(master, text="Body", font=('Calibri', 11)).grid(row=4, sticky=W, padx=5)
tk.Label(master, text="Attachment", font=('Calibri', 11)).grid(row=5, sticky=W, padx=5)
notifyLabel = tk.Label(master, text="", font=('Calibri', 11))
notifyLabel.grid(row=6, sticky=S, padx=5)

#storage
temp_To = StringVar()
temp_Subject = StringVar()
temp_Body = StringVar()
temp_Attachment = StringVar()

#entries
toEntry = Entry(master, textvariable=temp_To)
toEntry.grid(row=2, column=0)
subjectEntry = Entry(master, textvariable=temp_Subject)
subjectEntry.grid(row=3, column=0, padx=100)
bodyEntry = Entry(master, textvariable=temp_Body)
bodyEntry.grid(row=4, column=0)
attachmentEntry = Entry(master, textvariable=temp_Attachment)
attachmentEntry.grid(row=5, column=0)

#buttons
Button(master, text="Send", command=send).grid(row=6, sticky=W, pady=15, padx=5)
Button(master, text="Reset", command=reset).grid(row=6, sticky=W, pady=45, padx=70)


master.mainloop()
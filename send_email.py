from email.mime.text import MIMEText
from credentials import *
import smtplib

def send_email(email, height, color, average_height, rounded_pct, count):
    from_email = gmail_un
    from_password = gmail_pw
    to_email = email

    subject = "Height and color data"
    message = "Hey there, your height is <strong>%s</strong> and your eye color is <strong>%s</strong>. <br> Average height of all is <strong>%s</strong>. The percentage of users with your eye color is <strong>%s</strong>. These values are calculated out of <strong>%s</strong> people. <br><br> Thanks!" % (height, color, average_height, rounded_pct, count)

    msg = MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT', cast=int)
SMTP_USERNAME = config('SMTP_USERNAME')
SMTP_PASSWORD = config('SMTP_PASSWORD')
EMAIL_FROM = config('EMAIL_FROM')
EMAIL_SUBJECT = config('EMAIL_SUBJECT')

def send_account_activation_email(email: str, email_token: str):
    body = f"Hi, click on the link to activate your account http://127.0.0.1:8000/users/activate/{email_token}"
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = email
    msg['Subject'] = EMAIL_SUBJECT
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, email, msg.as_string())


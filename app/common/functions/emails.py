import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config
from fastapi import HTTPException

SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT', cast=int)
SMTP_USERNAME = config('SMTP_USERNAME')
SMTP_PASSWORD = config('SMTP_PASSWORD')
EMAIL_FROM = config('EMAIL_FROM')
EMAIL_SUBJECT = config('EMAIL_SUBJECT')

def send_account_activation_email(email: str, user_id: int):
    print(email, user_id)
    print(SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM, EMAIL_SUBJECT)

    body = f"Hi, click on the link to activate your account http://127.0.0.1:8000/users/activate/{user_id}"
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = email
    msg['Subject'] = EMAIL_SUBJECT
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, email, msg.as_string())
            server.close()
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to send activation email")



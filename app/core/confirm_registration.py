
from app.services.service_email import send_email
import random
import string


# def generate_verification_code():
#     letters_and_digits = string.ascii_letters + string.digits
#     return ''.join(random.choice(letters_and_digits) for _ in range(6))


subject = "Confirm Registration"

URL = "http://127.0.0.1:8000/mail_verification"

body = f"""Dear user,
            Thank you for creating your account.
            Please confirm your email address. The confirmation code is:
          {URL}

          If you have not requested a verification code, you can safely ignore this email․
          """

recipients = []


sender = "dinaras.alexander@gmail.com"

password = "password [email pin]"


def mail_verification_email(email):
    recipients.append(email)
    send_email(subject, body, sender, recipients, password)







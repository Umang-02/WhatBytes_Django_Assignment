from django.core.mail import send_mail
import uuid 
from authentication import settings
def send_forget_password_mail(email,token):
    subject="Your forget password Link"
    message=f'Hi! Click on the following link to reset your password http://127.0.0.1:8000/change-password/{token}'

    email_from=settings.EMAIL_HOST_USER
    email_to=[email]
    send_mail(subject,message,email_from,email_to)
    return True
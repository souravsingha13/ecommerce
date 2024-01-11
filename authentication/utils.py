from django.core.mail import send_mail
from django.conf import settings

def send_mail_to_client():
    subject = "Email verification"
    message = "This is a test email"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["souravsingha.one.direction@gmail.com"]
    
    send_mail(subject, message, from_email, recipient_list)
    
from django.core.mail import send_mail,EmailMessage
from django.conf import settings

def send_mail_to_client():
    subject = "Email verification"
    message = "This is a test email"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["souravsingha.one.direction@gmail.com"]
    
    send_mail(subject, message, from_email, recipient_list)
    
# def send_activation_email(user):
#     subject = "Email verification"
#     activation_link = reverse('activate_user', kwargs={'uidb64': user.pk, 'token': user.activation_token})  # Use reverse for URL generation
#     message = f"Please click the following link to activate your account:\n{activation_link}"
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [user.email]  # Use the user's email address

#     send_mail(subject, message, from_email, recipient_list)
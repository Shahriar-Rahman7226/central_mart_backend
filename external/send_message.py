from core import settings
from  apps.users.models import UserModel
from django.core.mail import send_mail
from django.conf import settings

# email and sms
def send_email(user_id=None, subject=None, body=None, request_user=None):
    if not user_id:
        user_id =request_user
    user_obj = UserModel.objects.get(id=user_id)

    mail_subject = subject
    message = f"Greetings {user_obj.first_name}!\n {body}"
    to_email = str(user_obj.email)
    email = send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False
    )
    if email:
        return ("Email sent")
    else:
        return ("Email failed")
    

def send_sms(user_obj):
    pass
from django.core.mail import send_mail
import random
from django.conf import settings
from .models import *


def send_otp(email):
    subject = 'Your account verification email'
    otp = random.randint(100000, 999999)
    message = 'Hey new user, Your otp is ' + str(otp) 
    email_from = settings.EMAIL_HOST_USER

    Token.objects.create(email=email, otp=otp)

    
    send_mail(
        subject, 
        message, 
        email_from,
        [email],
        fail_silently=False
    )
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

def send_mail_after_registration(email, token, username, request):
    subject = "Your account needs to be verified"
    message = render_to_string('gmail_verification_link.html', {
        'user': username,
        # 'domain': get_current_site(request).domain, 
        'domain': 'localhost:8000' or '127.0.0.1:8000', 
        'token': token,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print(message)
    send_mail(subject, message , email_from ,recipient_list)
    print("message is sent")
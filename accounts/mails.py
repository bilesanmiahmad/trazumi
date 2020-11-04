from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_formatted_email(user):
    subject = "Welcome to Trazumi Shopping App"
    from_email = settings.EMAIL_HOST_USER
    to = [user.email, 'fbilesanmi@gmail.com']
    text_content = "Thank you for joining us at Trazumi"
    html_content = '<h1>Thank you for joining us at Trazumi</h1>' \
                   '<p> It\'s a pleasure to have you on board, ' + \
                   user.first_name + '. This is the first step to buy all your groceries at ease.</p> ' \
                   '<p>Verification Code: ' + str(user.verification_pin) + ' </p>'
                   
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

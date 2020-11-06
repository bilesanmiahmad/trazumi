from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_formatted_email(user):
    subject = "Welcome to Trazumi Shopping App"
    from_email = settings.EMAIL_HOST_USER
    to = [user.email, 'fbilesanmi@gmail.com', 'pelumikayode@outlook.com']
    text_content = "Thank you for joining us at Trazumi"
    html_content = '<h1>Thank you for joining us at Trazumi</h1>' \
                   '<p> It\'s a pleasure to have you on board, ' + \
                   user.first_name + '. This is the first step to buy all your groceries at ease. Please proceed to verify your email with the code below to enjoy the Trazumi experience.</p> ' \
                   '<p>Verification Code: ' + str(user.verification_pin) + ' </p>'
                   
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_verification_email(user):
    subject = "Congratulations! You are verified!"
    from_email = settings.EMAIL_HOST_USER
    to = [user.email, 'fbilesanmi@gmail.com', 'pelumikayode@outlook.com']
    text_content = "You are now verified"
    html_content = '<h1>Awesome! You are now verified</h1>' \
                   '<p> It\'s a pleasure to have you on board, ' + \
                   user.first_name + '. You can now explore the amazing grocerices from various Nigerian stores close to you.</p> ' 
                   
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

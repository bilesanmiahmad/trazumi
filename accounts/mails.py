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


def send_forgot_password_email(user):
    subject = "Forgot your password?"
    from_email = settings.EMAIL_HOST_USER
    to = [user.email, 'fbilesanmi@gmail.com', 'pelumikayode@outlook.com']
    text_content = "Did you forget your password"
    html_content = '<h1>Did you request to change your password?</h1>' \
                   '<p> Hi ' + user.first_name + ', we got a request for you to change your password. In order to verify you requested ' \
                   'for this change, please verify your request using the verification key below.</p>' \
                   '<h3>Verification Code: ' + str(user.verification_pin) + '</h3>'
                   
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_change_password_email(user):
    subject = "Your password has been changed"
    from_email = settings.EMAIL_HOST_USER
    to = [user.email, 'fbilesanmi@gmail.com', 'pelumikayode@outlook.com']
    text_content = "Your password has been changed"
    html_content = '<h1>Congratulations, you have successfully changed your password</h1>' \
                   '<p> Congratulations' + user.first_name + ', you have changed your password. ' \
                   'You can get back on the Trazumi platform to enjoy your shopping experience.</p>' 
                   
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

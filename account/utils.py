# from django.core.mail import send_mail
#
#
# def send_activation_code(email, activation_code):
#     activation_url = f'http://localhost:8000/v1/api/account/activate/{activation_code}'
#     message = f"""
#         Thank you for signing up.
#         Please, activate your account.
#         Activation link: {activation_url}
#     """
#     send_mail(
#         'Activate your account',
#         message,
#         'test@test.com',
#         [email, ],
#         fail_silently=False
#     )











from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_activation_code(email, activation_code, status=None):
    if status == 'register':
        context = {
            'text_detail': "Thank you for registration!",
            "email": email,
            "domain": "http://localhost:8000",
            "activation_code": activation_code
        }
        msg_html = render_to_string('email.html', context)
        message = strip_tags(msg_html)
        send_mail(
            'Activate Your Account',
            message,
            'test_admin@gmail.com',
            [email, ],
            html_message=msg_html,
            fail_silently=False
        )
    elif status == 'reset_password':
        send_mail(
            'Reset Your password',
            f'Код активации: {activation_code}',
            'test_admin@gmail.com',
            [email, ],
            fail_silently=False
        )







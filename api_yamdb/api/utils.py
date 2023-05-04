from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api_yamdb.settings import DEFAULT_FROM_EMAIL


def send_confirmation_code(user):
    """Функция отправки кода подтверждения."""
    confirmation_code = default_token_generator.make_token(user)
    subject = 'YaMDB: код подтверждения'
    message = f'Ваш код для подтверждения: {confirmation_code}'
    from_mail = DEFAULT_FROM_EMAIL
    to_mail = [user.email]
    return send_mail(subject, message, from_mail, to_mail)

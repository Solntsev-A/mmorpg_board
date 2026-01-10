from datetime import timedelta
import random
from django.utils import timezone
from accounts.models import EmailConfirmation
from django.core.mail import send_mail
from django.conf import settings



CODE_TTL_MINUTES = 15


def generate_confirmation_code():
    return f"{random.randint(100000, 999999)}"


def create_email_confirmation(user):
    code = generate_confirmation_code()
    expires_at = timezone.now() + timedelta(minutes=CODE_TTL_MINUTES)

    confirmation = EmailConfirmation.objects.create(user=user, code=code, expires_at=expires_at)

    return confirmation


def send_confirmation_email(user, confirmation):
    subject = 'Подтверждение регистрации'
    message = (
        f'Здравствуйте!\n\n'
        f'Ваш код подтверждения регистрации:\n\n'
        f'{confirmation.code}\n\n'
        f'Код действителен до: {confirmation.expires_at.strftime("%d.%m.%Y %H:%M")}\n\n'
        f'Если вы не регистрировались — просто проигнорируйте это письмо.'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

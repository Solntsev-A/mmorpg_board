from datetime import timedelta
import random
from django.utils import timezone
from accounts.models import EmailConfirmation


CODE_TTL_MINUTES = 15


def generate_confirmation_code():
    return f"{random.randint(100000, 999999)}"


def create_email_confirmation(user):
    code = generate_confirmation_code()
    expires_at = timezone.now() + timedelta(minutes=CODE_TTL_MINUTES)

    confirmation = EmailConfirmation.objects.create(user=user, code=code, expires_at=expires_at)

    return confirmation

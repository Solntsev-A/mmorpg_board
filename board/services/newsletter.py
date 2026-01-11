from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User


def send_newsletter(newsletter):
    users = User.objects.filter(is_active=True)

    recipient_list = [user.email for user in users if user.email]

    if not recipient_list:
        return 0

    send_mail(
        subject=newsletter.subject,
        message=newsletter.content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    newsletter.is_sent = True
    newsletter.save()

    return len(recipient_list)

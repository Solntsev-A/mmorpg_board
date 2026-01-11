from django.core.mail import send_mail
from django.conf import settings


def send_new_response_notification(response):
    advertisement = response.advertisement
    author = advertisement.author

    subject = f'Новый отклик на объявление "{advertisement.title}"'
    message = (
        f'Доброго времени суток!\n\n'
        f'На ваше объявление "{advertisement.title}"'
        f'поступил новый отклик.\n\n'
        f'Текст отклика:\n'
        f'{response.text}\n\n'
        f'Зайдите в личный кабинет, чтобы принять или отклонить отклик.'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[author.email],
        fail_silently=False,
    )

def send_response_accepted_notification(response):
    user = response.author
    advertisement = response.advertisement

    subject = f'Ваш отклик принят'
    message = (
        f'Доброго времени суток!\n\n'
        f'Ваш отклик на объявление "{advertisement.title}" был принят.\n\n'
        f'Автор объявления скоро свяжется с вами.'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

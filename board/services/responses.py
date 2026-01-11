from django.core.exceptions import PermissionDenied as DjangoPermissionDenied

from board.models import Response
from board.services.notifications import send_new_response_notification, send_response_accepted_notification


class ResponseError(Exception):
    """Базовое исключение для ошибок откликов"""
    pass


class CannotRespondToOwnAdvertisement(ResponseError):
    """Пользователь пытается откликнуться на своё объявление"""
    pass


class ResponseAlreadyAccepted(ResponseError):
    """Отклик уже был принят"""
    pass


class PermissionDenied(ResponseError):
    """Нет прав на выполнение действия"""
    pass


def create_response(*, user, advertisement, text):
    if advertisement.author == user:
        raise CannotRespondToOwnAdvertisement(
            'Нельзя оставлять отклик на своё объявление'
        )

    response = Response.objects.create(
        author=user,
        advertisement=advertisement,
        text=text
    )

    send_new_response_notification(response)

    return response


def accept_response(*, response, user):
    if response.advertisement.author != user:
        raise PermissionDenied(
            'Вы не можете принять отклик на чужое объявление'
        )

    if response.is_accepted:
        raise ResponseAlreadyAccepted(
            'Этот отклик уже был принят'
        )

    response.is_accepted = True
    response.save()

    send_response_accepted_notification(response)

    return response

def delete_response(*, response, user):
    # Проверяем, что пользователь — автор объявления
    if response.advertisement.author != user:
        raise PermissionDenied(
            'Вы не можете удалить этот отклик'
        )

    response.delete()

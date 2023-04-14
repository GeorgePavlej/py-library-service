import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from requests import Response

from borrowings.models import Borrowing


def send_telegram_message(chat_id: int, message: str) -> Response:
    bot_token = settings.BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=payload)
    return response


@receiver(post_save, sender=Borrowing)
def send_borrowing_notification(instance, created, **kwargs) -> None:
    send_new_borrowing_notification(instance, created)


def send_new_borrowing_notification(instance, created=True) -> None:
    if created:
        chat_id = settings.CHAT_ID
        message = (
            f"New borrowing:\n"
            f"User: {instance.user}\n"
            f"Book: {instance.book}\n"
            f"Borrow Date: {instance.borrow_date}\n"
            f"Expected Return Date: {instance.expected_return_date}"
        )
        send_telegram_message(chat_id, message)

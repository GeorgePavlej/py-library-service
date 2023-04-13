import requests
from django.conf import settings
from requests import Response


def send_telegram_message(chat_id: int, message: str) -> Response:
    bot_token = settings.BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=payload)
    return response


def send_new_borrowing_notification(borrowing):
    chat_id = settings.CHAT_ID
    message = (
        f"New borrowing:\n"
        f"User: {borrowing.user}\n"
        f"Book: {borrowing.book}\n"
        f"Borrow Date: {borrowing.borrow_date}\n"
        f"Expected Return Date: {borrowing.expected_return_date}"
    )
    send_telegram_message(chat_id, message)

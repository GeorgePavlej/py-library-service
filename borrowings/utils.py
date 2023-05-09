from datetime import date

from django.conf import settings
from django.db.models import Q

from borrowings.models import Borrowing
from borrowings.signals import send_telegram_message


def check_overdue_borrowings() -> None:
    overdue_borrowings = Borrowing.objects.filter(
        Q(expected_return_date__lte=date.today()) &
        Q(actual_return_date__isnull=True)
    )

    if not overdue_borrowings.exists():
        message = "No borrowings overdue today!"
        send_telegram_message(chat_id=settings.CHAT_ID, message=message)
        return

    for borrowing in overdue_borrowings:
        message = (
            f"Overdue borrowing:\n"
            f"User: {borrowing.user}\n"
            f"Book: {borrowing.book}\n"
            f"Borrow Date: {borrowing.borrow_date}\n"
            f"Expected Return Date: {borrowing.expected_return_date}"
        )
        send_telegram_message(chat_id=settings.CHAT_ID, message=message)

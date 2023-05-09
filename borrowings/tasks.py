from celery import shared_task
from .utils import check_overdue_borrowings


@shared_task
def check_overdue_borrowings_task() -> None:
    check_overdue_borrowings()

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from borrowings.models import Borrowing
from borrowings.utils import send_telegram_message


@receiver(post_save, sender=Borrowing)
def send_borrowing_notification(
        instance: Borrowing,
        created: bool, **kwargs
) -> None:
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


@receiver(post_save, sender=Borrowing)
def update_inventory_on_borrowing_create(
        sender, instance: Borrowing, created: bool, **kwargs
) -> None:
    if created:
        book = instance.book
        book.inventory -= 1
        book.save()


@receiver(post_delete, sender=Borrowing)
def update_inventory_on_borrowing_delete(
        sender, instance: Borrowing, **kwargs) -> None:
    book = instance.book
    book.inventory += 1
    book.save()

from django.core.management.base import BaseCommand
from user.models import User


class Command(BaseCommand):
    help = "Create a test user for development purposes"

    def handle(self, *args, **options):
        email = "testuser@example.com"
        password = "testpassword123"

        if not User.objects.filter(email=email).exists():
            User.objects.create_user(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Test user created: {email}"))
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Test user with email '{email}' already exists"
                )
            )

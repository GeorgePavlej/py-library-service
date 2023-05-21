# Generated by Django 4.2 on 2023-05-21 18:08

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrowing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "borrow_date",
                    models.DateField(
                        default=django.utils.timezone.now,
                        validators=[
                            django.core.validators.MinValueValidator(
                                datetime.date(2023, 5, 21)
                            )
                        ],
                    ),
                ),
                (
                    "expected_return_date",
                    models.DateField(
                        default=django.utils.timezone.now,
                        validators=[
                            django.core.validators.MinValueValidator(
                                datetime.date(2023, 5, 21)
                            )
                        ],
                    ),
                ),
                (
                    "actual_return_date",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(
                                datetime.date(2023, 5, 21)
                            )
                        ],
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="books.book"
                    ),
                ),
            ],
        ),
    ]

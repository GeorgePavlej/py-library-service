# Generated by Django 4.2 on 2023-05-25 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("borrowings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                    "status",
                    models.CharField(
                        choices=[("Pending", "Pending"), ("Paid", "Paid")],
                        default="Pending",
                        max_length=10,
                    ),
                ),
                (
                    "payment_type",
                    models.CharField(
                        choices=[("Payment", "Payment"), ("Fine", "Fine")],
                        default="Payment",
                        max_length=10,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("session_url", models.URLField(blank=True, max_length=360, null=True)),
                ("session_id", models.TextField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "borrowing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="borrowings.borrowing",
                    ),
                ),
            ],
        ),
    ]

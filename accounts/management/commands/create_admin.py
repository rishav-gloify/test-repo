import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Create or update an admin user from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_ADMIN_USERNAME") or os.environ.get(
            "DJANGO_SUPERUSER_USERNAME"
        )
        email = os.environ.get("DJANGO_ADMIN_EMAIL") or os.environ.get(
            "DJANGO_SUPERUSER_EMAIL", ""
        )
        password = os.environ.get("DJANGO_ADMIN_PASSWORD") or os.environ.get(
            "DJANGO_SUPERUSER_PASSWORD"
        )

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping admin creation: set DJANGO_ADMIN_USERNAME and "
                    "DJANGO_ADMIN_PASSWORD."
                )
            )
            return

        User = get_user_model()
        admin_defaults = {
            "email": email,
            "role": User.Roles.ADMIN,
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        }

        with transaction.atomic():
            user, created = User.objects.get_or_create(
                username=username,
                defaults=admin_defaults,
            )

            for field, value in admin_defaults.items():
                setattr(user, field, value)

            user.set_password(password)
            user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} admin user '{username}'."))

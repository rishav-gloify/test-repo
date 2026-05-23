from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)

    @property
    def is_librarian(self):
        return self.role == self.Roles.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_student(self):
        return self.role == self.Roles.STUDENT

from django.core.exceptions import ValidationError
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    class AvailabilityStatus(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        UNAVAILABLE = "UNAVAILABLE", "Unavailable"

    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books")
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    category = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField(default=1)
    availability_status = models.CharField(
        max_length=20,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.AVAILABLE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title", "author__name"]

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    @property
    def active_issue_count(self):
        if not self.pk:
            return 0
        return self.issues.filter(return_date__isnull=True).count()

    @property
    def available_copies(self):
        return max(self.quantity - self.active_issue_count, 0)

    def clean(self):
        if self.quantity < 0:
            raise ValidationError({"quantity": "Quantity cannot be negative."})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_availability_status()

    def refresh_availability_status(self):
        status = (
            self.AvailabilityStatus.AVAILABLE
            if self.available_copies > 0
            else self.AvailabilityStatus.UNAVAILABLE
        )
        if self.availability_status != status:
            self.availability_status = status
            Book.objects.filter(pk=self.pk).update(availability_status=status)

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from books.models import Book


class IssueRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issues")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issue_records",
    )
    issue_date = models.DateField(default=timezone.localdate)
    return_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-issue_date", "-created_at"]

    def __str__(self):
        return f"{self.book.title} issued to {self.student.username}"

    @property
    def is_returned(self):
        return self.return_date is not None

    def clean(self):
        errors = {}
        if self.student_id and not self.student.is_student:
            errors["student"] = "Books can only be issued to student users."
        if self.return_date and self.return_date < self.issue_date:
            errors["return_date"] = "Return date cannot be earlier than issue date."
        if not self.pk and self.book_id and self.book.available_copies <= 0:
            errors["book"] = "No copies are currently available for this book."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.book.refresh_availability_status()

    def mark_returned(self):
        if not self.return_date:
            self.return_date = timezone.localdate()
            self.save(update_fields=["return_date", "updated_at"])
        return self

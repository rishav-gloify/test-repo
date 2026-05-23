from django import forms
from django.contrib.auth import get_user_model

from books.models import Book
from transactions.models import IssueRecord


class IssueBookForm(forms.ModelForm):
    class Meta:
        model = IssueRecord
        fields = ("book", "student", "issue_date")
        widgets = {
            "book": forms.Select(attrs={"class": "form-select"}),
            "student": forms.Select(attrs={"class": "form-select"}),
            "issue_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = Book.objects.filter(
            availability_status=Book.AvailabilityStatus.AVAILABLE
        )
        self.fields["student"].queryset = get_user_model().objects.filter(
            role=get_user_model().Roles.STUDENT,
            is_active=True,
        )

    def clean_book(self):
        book = self.cleaned_data["book"]
        if book.available_copies <= 0:
            raise forms.ValidationError("No copies are currently available for this book.")
        return book

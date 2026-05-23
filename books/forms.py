from django import forms

from books.models import Author, Book


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Author name"}
            ),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "author", "isbn", "category", "quantity")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.Select(attrs={"class": "form-select searchable-author-select"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity

import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from transactions.forms import IssueBookForm
from transactions.models import IssueRecord


class LibraryAdminRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_librarian


class IssueBookView(LoginRequiredMixin, LibraryAdminRequiredMixin, CreateView):
    model = IssueRecord
    form_class = IssueBookForm
    template_name = "transactions/issue_form.html"
    success_url = reverse_lazy("transactions:issued")

    def form_valid(self, form):
        messages.success(self.request, "Book issued successfully.")
        return super().form_valid(form)


class IssuedBooksView(LoginRequiredMixin, ListView):
    model = IssueRecord
    template_name = "transactions/issued_books.html"
    context_object_name = "records"
    paginate_by = 10

    def get_queryset(self):
        queryset = IssueRecord.objects.select_related("book__author", "student")
        if self.request.user.is_librarian:
            return queryset
        return queryset.filter(student=self.request.user)


class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        record = get_object_or_404(IssueRecord.objects.select_related("book", "student"), pk=pk)
        if not request.user.is_librarian and record.student_id != request.user.id:
            raise PermissionDenied("You can only return your own issued books.")
        record.mark_returned()
        messages.success(request, "Book returned successfully.")
        return redirect("transactions:issued")


class IssuedBooksExportView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = IssueRecord.objects.select_related("book__author", "student")
        if not request.user.is_librarian:
            queryset = queryset.filter(student=request.user)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="issued_books.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "Book",
                "Author",
                "ISBN",
                "Student",
                "Issue Date",
                "Return Date",
                "Status",
            ]
        )
        for record in queryset:
            writer.writerow(
                [
                    record.book.title,
                    record.book.author.name,
                    record.book.isbn,
                    record.student.username,
                    record.issue_date,
                    record.return_date or "",
                    "Returned" if record.is_returned else "Issued",
                ]
            )
        return response

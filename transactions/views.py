from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
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
        queryset = IssueRecord.objects.select_related("book", "student")
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

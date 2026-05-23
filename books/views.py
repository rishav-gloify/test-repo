import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from books.forms import AuthorForm, BookForm
from books.models import Author, Book


class LibraryAdminRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_librarian


def get_filtered_books(request, restrict_to_student=False):
    queryset = Book.objects.select_related("author")
    if restrict_to_student and not request.user.is_librarian:
        queryset = queryset.filter(issues__student=request.user).distinct()
    query = request.GET.get("q", "").strip()
    author_id = request.GET.get("author", "").strip()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(author__name__icontains=query)
            | Q(category__icontains=query)
            | Q(isbn__icontains=query)
        )
    if author_id:
        queryset = queryset.filter(author_id=author_id)
    return queryset


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        return get_filtered_books(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        context["authors"] = Author.objects.all()
        context["selected_author"] = self.request.GET.get("author", "").strip()
        return context


class BookCreateView(LoginRequiredMixin, LibraryAdminRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:list")

    def form_valid(self, form):
        messages.success(self.request, "Book added successfully.")
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, LibraryAdminRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:list")

    def form_valid(self, form):
        messages.success(self.request, "Book updated successfully.")
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, LibraryAdminRequiredMixin, DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("books:list")

    def form_valid(self, form):
        messages.success(self.request, "Book deleted successfully.")
        return super().form_valid(form)


class BookExportView(LoginRequiredMixin, View):
    def get(self, request):
        books = get_filtered_books(request, restrict_to_student=True)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="books.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "Title",
                "Author",
                "ISBN",
                "Category",
                "Quantity",
                "Available Copies",
                "Availability Status",
            ]
        )
        for book in books:
            writer.writerow(
                [
                    book.title,
                    book.author.name,
                    book.isbn,
                    book.category,
                    book.quantity,
                    book.available_copies,
                    book.get_availability_status_display(),
                ]
            )
        return response


class AuthorListView(LoginRequiredMixin, LibraryAdminRequiredMixin, ListView):
    model = Author
    template_name = "books/author_list.html"
    context_object_name = "authors"
    paginate_by = 10

    def get_queryset(self):
        queryset = Author.objects.annotate(book_count=Count("books")).order_by("name")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        return context


class AuthorCreateView(LoginRequiredMixin, LibraryAdminRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "books/author_form.html"
    success_url = reverse_lazy("books:authors")

    def form_valid(self, form):
        messages.success(self.request, "Author added successfully.")
        return super().form_valid(form)


class AuthorUpdateView(LoginRequiredMixin, LibraryAdminRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "books/author_form.html"
    success_url = reverse_lazy("books:authors")

    def form_valid(self, form):
        messages.success(self.request, "Author updated successfully.")
        return super().form_valid(form)


class AuthorDeleteView(LoginRequiredMixin, LibraryAdminRequiredMixin, DeleteView):
    model = Author
    template_name = "books/author_confirm_delete.html"
    success_url = reverse_lazy("books:authors")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "This author cannot be deleted because books are linked to them.",
            )
            return redirect("books:authors")
        messages.success(self.request, "Author deleted successfully.")
        return response

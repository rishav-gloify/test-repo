from django.urls import path

from books.views import (
    AuthorCreateView,
    AuthorDeleteView,
    AuthorListView,
    AuthorUpdateView,
    BookCreateView,
    BookDeleteView,
    BookExportView,
    BookListView,
    BookUpdateView,
)


app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="list"),
    path("export/", BookExportView.as_view(), name="export"),
    path("add/", BookCreateView.as_view(), name="add"),
    path("authors/", AuthorListView.as_view(), name="authors"),
    path("authors/add/", AuthorCreateView.as_view(), name="author_add"),
    path("authors/<int:pk>/edit/", AuthorUpdateView.as_view(), name="author_edit"),
    path("authors/<int:pk>/delete/", AuthorDeleteView.as_view(), name="author_delete"),
    path("<int:pk>/edit/", BookUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name="delete"),
]

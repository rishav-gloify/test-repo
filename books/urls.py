from django.urls import path

from books.views import BookCreateView, BookDeleteView, BookListView, BookUpdateView


app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="list"),
    path("add/", BookCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", BookUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name="delete"),
]

from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from accounts.permissions import IsLibraryAdminOrReadOnly
from books.models import Author, Book
from books.serializers import AuthorSerializer, BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
    permission_classes = [IsLibraryAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["title", "author__name", "category", "isbn"]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibraryAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["name"]

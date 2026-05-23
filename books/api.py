from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from accounts.permissions import IsLibraryAdminOrReadOnly
from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibraryAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["title", "author", "category", "isbn"]

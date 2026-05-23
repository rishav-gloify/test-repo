from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    available_copies = serializers.IntegerField(read_only=True)
    active_issue_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "isbn",
            "category",
            "quantity",
            "availability_status",
            "available_copies",
            "active_issue_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "availability_status", "created_at", "updated_at")

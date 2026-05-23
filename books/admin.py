from django.contrib import admin

from books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "isbn",
        "category",
        "quantity",
        "availability_status",
    )
    list_filter = ("availability_status", "category")
    search_fields = ("title", "author", "isbn", "category")
    readonly_fields = ("availability_status", "created_at", "updated_at")

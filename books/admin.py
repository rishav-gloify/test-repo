from django.contrib import admin

from books.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


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
    list_filter = ("availability_status", "category", "author")
    search_fields = ("title", "author__name", "isbn", "category")
    readonly_fields = ("availability_status", "created_at", "updated_at")
    autocomplete_fields = ("author",)

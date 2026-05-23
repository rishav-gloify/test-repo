from django.contrib import admin

from transactions.models import IssueRecord


@admin.register(IssueRecord)
class IssueRecordAdmin(admin.ModelAdmin):
    list_display = ("book", "student", "issue_date", "return_date", "is_returned")
    list_filter = ("issue_date", "return_date")
    search_fields = ("book__title", "book__isbn", "student__username", "student__email")
    autocomplete_fields = ("book", "student")

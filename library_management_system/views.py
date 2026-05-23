from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render

from books.models import Book
from transactions.models import IssueRecord


@login_required
def dashboard(request):
    books = Book.objects.annotate(
        active_issue_total=Count("issues", filter=Q(issues__return_date__isnull=True))
    )
    available_books = sum(max(book.quantity - book.active_issue_total, 0) for book in books)

    context = {
        "total_books": books.count(),
        "issued_books": IssueRecord.objects.filter(return_date__isnull=True).count(),
        "available_books": available_books,
        "registered_users": get_user_model().objects.count(),
    }
    return render(request, "dashboard.html", context)

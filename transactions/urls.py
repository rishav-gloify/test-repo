from django.urls import path

from transactions.views import (
    IssueBookView,
    IssuedBooksExportView,
    IssuedBooksView,
    ReturnBookView,
)


app_name = "transactions"

urlpatterns = [
    path("issue/", IssueBookView.as_view(), name="issue"),
    path("issued/", IssuedBooksView.as_view(), name="issued"),
    path("issued/export/", IssuedBooksExportView.as_view(), name="issued_export"),
    path("<int:pk>/return/", ReturnBookView.as_view(), name="return"),
]

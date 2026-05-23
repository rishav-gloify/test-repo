from django.urls import path

from transactions.views import IssueBookView, IssuedBooksView, ReturnBookView


app_name = "transactions"

urlpatterns = [
    path("issue/", IssueBookView.as_view(), name="issue"),
    path("issued/", IssuedBooksView.as_view(), name="issued"),
    path("<int:pk>/return/", ReturnBookView.as_view(), name="return"),
]

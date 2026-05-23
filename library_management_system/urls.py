from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.api import UserViewSet
from books.api import AuthorViewSet, BookViewSet
from library_management_system.views import dashboard
from transactions.api import IssueRecordViewSet


router = DefaultRouter()
router.register("books", BookViewSet, basename="api-books")
router.register("authors", AuthorViewSet, basename="api-authors")
router.register("users", UserViewSet, basename="api-users")
router.register("issues", IssueRecordViewSet, basename="api-issues")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("accounts/", include("accounts.urls")),
    path("books/", include("books.urls")),
    path("transactions/", include("transactions.urls")),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]

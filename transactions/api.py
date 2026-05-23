from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from transactions.models import IssueRecord
from transactions.serializers import IssueRecordSerializer


class IssueRecordViewSet(ModelViewSet):
    serializer_class = IssueRecordSerializer

    def get_queryset(self):
        queryset = IssueRecord.objects.select_related("book", "student")
        if self.request.user.is_librarian:
            return queryset
        return queryset.filter(student=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_librarian:
            raise PermissionDenied("Only admins can issue books.")
        serializer.save()

    def perform_update(self, serializer):
        if not self.request.user.is_librarian:
            raise PermissionDenied("Only admins can update issue records.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_librarian:
            raise PermissionDenied("Only admins can delete issue records.")
        instance.delete()

    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        record = self.get_object()
        if not request.user.is_librarian and record.student_id != request.user.id:
            raise PermissionDenied("You can only return your own issued books.")
        record.mark_returned()
        serializer = self.get_serializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

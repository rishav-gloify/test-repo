from django.utils import timezone
from rest_framework import serializers

from transactions.models import IssueRecord


class IssueRecordSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    student_username = serializers.CharField(source="student.username", read_only=True)
    is_returned = serializers.BooleanField(read_only=True)

    class Meta:
        model = IssueRecord
        fields = (
            "id",
            "book",
            "book_title",
            "student",
            "student_username",
            "issue_date",
            "return_date",
            "is_returned",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        issue_date = attrs.get("issue_date")
        if issue_date is None:
            issue_date = self.instance.issue_date if self.instance else timezone.localdate()

        instance = IssueRecord(
            book=attrs.get("book", self.instance.book if self.instance else None),
            student=attrs.get("student", self.instance.student if self.instance else None),
            issue_date=issue_date,
            return_date=attrs.get("return_date", self.instance.return_date if self.instance else None),
        )
        if self.instance:
            instance.pk = self.instance.pk
        instance.clean()
        return attrs

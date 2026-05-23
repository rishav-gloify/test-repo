from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from accounts.permissions import IsLibraryAdmin
from accounts.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.order_by("username")
    serializer_class = UserSerializer
    permission_classes = [IsLibraryAdmin]

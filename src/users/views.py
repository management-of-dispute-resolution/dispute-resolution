from djoser.views import UserViewSet

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet

from disputes.models import Dispute
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from .serializers import DisputeSerializer


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class DisputeViewSet(ModelViewSet):
    queryset = Dispute.objects.all()
    serializer_class = DisputeSerializer

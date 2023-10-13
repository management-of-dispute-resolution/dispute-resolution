from djoser.serializers import UserSerializer

from users.models import CustomUser


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

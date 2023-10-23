from djoser.serializers import UserSerializer
from rest_framework import serializers

from disputes.models import Comment, Dispute
from users.models import CustomUser


class CustomUserSerializer(UserSerializer):
    """Serializer for the CustomUser model."""

    class Meta:
        """
        Meta class CustomUserSerializer.

        Attributes:
            model: The CustomUser model class to be serialized.
            fields: A string indicating to include all fields
            from the CustomUser model.
        """

        model = CustomUser
        fields = ['email', 'password', 'first_name',
                  'last_name', 'phone_number', 'role']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""

    class Meta:
        """
        Meta class for CommentSerializer.

        Attributes:
            model: The Comment model class to be serialized.
            fields: A string indicating to include all fields
            from the Comment model.
        """

        model = Comment
        fields = ('id', 'sender', 'content', 'dispute', 'created_at', 'file')
        read_only_fields = ('sender', 'dispute', 'created_at')


class DisputeSerializer(serializers.ModelSerializer):
    """Serializer for the Dispute model."""

    class Meta:
        """
        Meta class DisputetSerializer.

        Attributes:
            model: The Dispute model class to be serialized.
            fields: A string indicating to include all fields
            from the Dispute model.
        """

        model = Dispute
        fields = (
            'id',
            'creator',
            'description',
            'created_at',
            'file',
            'closed_at',
            'opponent',
            'add_opponent',
            'status',
            'comments'
        )
        read_only_fields = (
            'creator',
            'created_at',
            'closed_at',
            'status',
            'add_opponent'
            'status',
            'comments'
        )


class PatchDisputeSerializer(serializers.ModelSerializer):
    """Serializer for PATCH request of the Dispute model."""

    class Meta:
        """
        Meta class DisputetSerializer.

        Attributes:
            model: The Dispute model class to be serialized.
            fields: A string indicating to include all fields
            from the Dispute model.
        """

        model = Dispute
        fields = (
            'id',
            'creator',
            'description',
            'created_at',
            'file',
            'closed_at',
            'opponent',
            'add_opponent',
            'status',
            'comments'
        )
        read_only_fields = (
            'creator',
            'created_at',
            'closed_at',
            'comments'
        )

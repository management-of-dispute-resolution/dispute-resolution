from djoser.serializers import UserSerializer
from rest_framework import serializers

from disputes.models import Comment, Dispute, FileDispute
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
        fields = ['email', 'id', 'first_name',
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
        fields = ('id', 'sender', 'content', 'dispute', 'created_at')
        read_only_fields = ('sender', 'dispute', 'created_at')


class FileDisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileDispute
        fields = "__all__"


class DisputeSerializer(serializers.ModelSerializer):
    """Serializer for the Dispute model."""

    last_comment = serializers.SerializerMethodField()
    file = FileDisputeSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

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
            'comments',
            'last_comment',
            'uploaded_files'
        )
        read_only_fields = (
            'creator',
            'created_at',
            'closed_at',
            'status',
            'add_opponent'
            'status',
            'comments',
            'last_comment',
        )

    def get_last_comment(self, obj):
        """Get the last comment."""
        last_comment = obj.comments.last()  # Получаем последний комментарий
        if last_comment:
            return CommentSerializer(last_comment).data
        return None

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', None)
        opponent = validated_data.pop('opponent', None)
        dispute = Dispute.objects.create(**validated_data)
        if uploaded_files:
            for file in uploaded_files:
                FileDispute.objects.create(
                    dispute=dispute,
                    file=file
                )
        if opponent:
            dispute.opponent.add(*opponent)
            dispute.save()
        return dispute


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

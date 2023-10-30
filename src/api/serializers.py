from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.permissions import SAFE_METHODS

from disputes.models import Comment, Dispute, FileComment, FileDispute
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


class FileCommentSerializer(serializers.ModelSerializer):
    """Serializer for the File in comment."""

    class Meta:
        model = FileComment
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""

    file = FileCommentSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        """
        Meta class for CommentSerializer.

        Attributes:
            model: The Comment model class to be serialized.
            fields: A string indicating to include all fields
            from the Comment model.
        """

        model = Comment
        fields = ('id', 'sender', 'file', 'uploaded_files',
                  'content', 'dispute', 'created_at')
        read_only_fields = ('sender', 'dispute', 'created_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'request' in self.context:
            method = self.context['request'].method
            if method in SAFE_METHODS:
                self.fields['sender'] = CustomUserSerializer(read_only=True)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        """Create the comment."""
        uploaded_files = validated_data.pop('uploaded_files', None)
        comment = Comment.objects.create(**validated_data)
        if uploaded_files:
            for file in uploaded_files:
                FileComment.objects.create(
                    comment=comment,
                    file=file
                )
        return comment


class FileDisputeSerializer(serializers.ModelSerializer):
    """Serializer for the File in dispute."""

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
    comments = CommentSerializer(many=True, read_only=True)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'request' in self.context:
            method = self.context['request'].method
            if method in SAFE_METHODS:
                self.fields['creator'] = CustomUserSerializer(read_only=True)
                self.fields['opponent'] = CustomUserSerializer(many=True)
        super().__init__(*args, **kwargs)

    def get_last_comment(self, obj):
        """Get the last comment."""
        last_comment = obj.comments.last()  # Получаем последний комментарий
        if last_comment:
            return CommentSerializer(last_comment).data
        return None

    def create(self, validated_data):
        """Create the dispute."""
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

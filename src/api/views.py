from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.permissions import IsMediatorAuthorOrOpponent
from api.serializers import (
    CommentSerializer,
    CustomUserSerializer,
    DisputeSerializer,
)
from disputes.models import Comment, Dispute
from users.models import CustomUser


class CustomUserViewSet(UserViewSet):
    """A viewset that provides CRUD operations for users."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class DisputeViewSet(ModelViewSet):
    """A viewset that provides CRUD operations for disputes."""

    queryset = Dispute.objects.all()
    serializer_class = DisputeSerializer
    permission_classes = [IsMediatorAuthorOrOpponent]


class CommentViewSet(ModelViewSet):
    """
    A viewset that provides CRUD operations for comments.

        Attributes:
        A queryset that retrieves all Comment instances.
        The serializer class used for Comment instances.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailViewSet(ViewSet):
    """
    Retrieve a single comment by its primary key (ID).

    Attributes:
    - A list of permissions that control access to this viewset.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, pk=None):
        """
        Retrieve a Comment instance by its primary key (ID).

        Args:
            request: The request object.
            pk: The primary key of the comment to retrieve.

        Returns:
            A Response object containing
            the serialized Comment data.

        Raises:
            Http404: If the comment with the given
            primary key does not exist.
        """
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def destroy(self, request, pk=None):  # нужна ли данная функция?
        """
        Delete a Comment instance by its primary key (ID).

        Args:
            request: The request object.
            pk: The primary key of the comment to delete.

        Returns:
            A Response indicating the successful deletion.

        Raises:
            Http404: If the comment with the given primary key does not exist.
        """
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

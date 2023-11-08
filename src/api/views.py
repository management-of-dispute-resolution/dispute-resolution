from datetime import datetime

from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.mixins import CreteListModelViewSet
from api.permissions import (
    IsCreatorOrMediatorOrOpponent,
    IsSenderOrMediatorOrDisputeCreator,
)
from api.serializers import (
    CommentSerializer,
    CustomUserSerializer,
    DisputeSerializer,
    PatchDisputeSerializer,
)
from disputes.models import Comment, Dispute
from users.models import CustomUser


class CustomUserViewSet(UserViewSet):
    """A viewset that provides CRUD operations for users."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


def check_opponent(func):
    """
    Ensure the request user does not set themselves as an opponent.

    A decorator that checks if
    the request user is attempting to
    set themselves as an opponent.
    """

    def wrapper(self, request, *args, **kwargs):
        opponent_ids = request.data.get('opponent', [])
        opponent_ids = [int(opponent_id) for opponent_id in opponent_ids]
        if request.user.id in opponent_ids:
            return Response(
                {'opponent': ['You cannot set yourself as an opponent.']},
                status=status.HTTP_400_BAD_REQUEST
            )

        return func(self, request, *args, **kwargs)

    return wrapper


class DisputeViewSet(ModelViewSet):
    """A viewset that provides CRUD operations for disputes."""

    serializer_class = DisputeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsCreatorOrMediatorOrOpponent,)
    parser_class = [MultiPartParser, FormParser]

    def get_queryset(self):
        """Change the queryset for DisputeViewSet."""
        user = self.request.user
        if user.is_authenticated:
            if user.is_mediator:
                return Dispute.objects.all()
            else:
                return (user.disputes_creator.all()
                    | user.disputes_opponent.filter(add_opponent=True)
                    ).distinct()
        else:
            return Dispute.objects.none()

    @check_opponent
    def create(self, request, *args, **kwargs):
        """Change the POST request for DisputeViewSet."""
        serializer = DisputeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_opponent
    def partial_update(self, request, pk=None):
        """Change the PATCH request for DisputeViewSet."""
        dispute = Dispute.objects.get(id=pk)
        dispute_status = request.data.get('status')
        data = self.request.data
        user = self.request.user

        if user.is_authenticated  and (
            user == dispute.creator
            or user.is_mediator
        ):
            if user != dispute.creator and 'description' in data:
                return Response(
                    {'description': ['Mediator cannot change description.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            elif not user.is_mediator and 'status' in data:
                return Response(
                    {'status': ['Author cannot change status.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            elif dispute.creator == user and dispute.status != 'not_started':
                return Response(
                    {'status': [('Author cannot make changes if '
                                 'status is not "not_started".')]},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                    {'description': ['You do not have the right to change the dispute.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if dispute_status == 'closed':
            data['closed_at'] = datetime.now()
        else:
            dispute.closed_at = None
        serializer = PatchDisputeSerializer(dispute, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(CreteListModelViewSet):
    """
    A viewset that provides CRUD operations for comments.

        Attributes:
        A queryset that retrieves all Comment instances.
        The serializer class used for Comment instances.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsSenderOrMediatorOrDisputeCreator,)
    parser_class = [MultiPartParser, FormParser]

    def get_queryset(self):
        """Change the queryset for CommentViewSet."""
        dispute_id = self.kwargs.get('dispute_id')
        dispute = get_object_or_404(Dispute, id=dispute_id)
        new_queryset = dispute.comments.all()
        user = self.request.user
        if user.is_authenticated:
            if (user.is_mediator or dispute.creator == user
                or (dispute.add_opponent == True and dispute.opponent == user)
            ):
                return new_queryset
        else:
            return Comment.objects.none()

    def perform_create(self, serializer):
        """Change the POST request for CommentViewSet."""
        dispute_id = self.kwargs.get('dispute_id')
        dispute = get_object_or_404(Dispute, id=dispute_id)
        serializer.save(sender=self.request.user, dispute=dispute)

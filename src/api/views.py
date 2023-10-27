from datetime import datetime

from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.mixins import CreteListModelViewSet
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


class DisputeViewSet(ModelViewSet):
    """A viewset that provides CRUD operations for disputes."""

    serializer_class = DisputeSerializer
    parser_class = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        print('hieeeeeeeee')

        if user.is_mediator:
            return Dispute.objects.all()
        elif user.is_authenticated:
            return (user.disputes_creator.all()
                    | user.disputes_opponent.filter(add_opponent=True))
        else:
            return Dispute.objects.none()

    def create(self, request, *args, **kwargs):
        """Change the POST request for DisputeViewSet."""
        print('h1333333333333')
        print(dir(request))
        print(request.data)
        serializer = DisputeSerializer(data=request.data)
        print('11111111111111111111')
        if serializer.is_valid():
            print(444444444)
            user1 = CustomUser.objects.get(id=1)
            print(user1)
            serializer.save(creator=self.request.user, opponent=user1)
            print(66666666666666)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Change the PATCH request for DisputeViewSet."""
        dispute = Dispute.objects.get(id=pk)
        dispute_status = request.data.get('status')
        data = request.data
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

    def get_queryset(self):
        """Change the queryset for CommentViewSet."""
        dispute_id = self.kwargs.get('dispute_id')
        dispute = get_object_or_404(Dispute, id=dispute_id)
        new_queryset = dispute.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        """Change the POST request for CommentViewSet."""
        dispute_id = self.kwargs.get('dispute_id')
        dispute = get_object_or_404(Dispute, id=dispute_id)
        serializer.save(sender=self.request.user, dispute=dispute)

from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, BasePermission

from disputes.models import Dispute


class IsCreatorOrMediatorOrOpponent(BasePermission):
    """
    Permission rule based on authorship or mediator status.

    Allows authors to modify and delete objects,
    mediators to perform any actions,
    and other users to perform only safe methods (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        """Check whether the user has permission to access the request."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check whether the user has permission to access the object."""
        if (
            obj.creator == request.user
            or request.user.is_mediator
            or request.method in SAFE_METHODS
        ):
            return True
        return False


class CommentsPermission(BasePermission):
    """
    Permission rule based on authorship, oppponent or mediator status.

    Allows authors, mediators, opponents to leave comments on the dispute.
    """

    def has_permission(self, request, view):
        """Check whether the user has permission to access the request."""
        dispute_id = view.kwargs.get('dispute_id')
        dispute = get_object_or_404(Dispute, id=dispute_id)

        user = request.user
        is_opponent = dispute.opponent.filter(id=user.id).exists()

        return (
            (is_opponent and dispute.add_opponent)
            or user == dispute.creator
            or user.is_mediator
        )

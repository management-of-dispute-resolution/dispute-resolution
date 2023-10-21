from rest_framework import permissions


class IsMediatorAuthorOrOpponent(permissions.BasePermission):
    """This class checks whether a user is a mediator, author, or opponent."""

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        Args:
            request (HttpRequest): The request object.
            view (View): The view to be accessed.

        Returns:
            bool: True if the user is a mediator,
            author, or opponent, and False otherwise.
        """
        if request.user.is_authenticated:
            return (
                request.user.is_mediator or
                request.user.is_author or
                request.user.is_opponent
            )

from rest_framework import permissions


class IsAuthorOrMediatorOrReadOnly(permissions.BasePermission):
    """
    Permission rule based on authorship or mediator status.

    Allows authors to modify and delete objects,
    mediators to perform any actions,
    and other users to perform only safe methods (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the user has permission to access the object.

        Parameters:
        - request: The request object.
        - view: The view object.
        - obj: The object the request is made to.

        Returns:
        - bool: True if the user has permission, otherwise False.
        """
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or request.user.is_mediator
        )

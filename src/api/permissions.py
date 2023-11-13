from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCreatorOrMediatorOrOpponent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if (obj.creator == request.user
            or request.user.is_mediator
            or request.method in SAFE_METHODS
        ):
            return True
        return False

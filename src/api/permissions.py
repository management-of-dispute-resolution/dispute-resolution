from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCreatorOrMediatorOrOpponent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated == True

    def has_object_permission(self, request, view, obj):
        if (obj.creator == request.user
            or request.user.is_mediator
        ):
            return True
        elif request.method in SAFE_METHODS:
            return True
        else:
            return False                 

class IsSenderOrMediatorOrDisputeCreator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated == True
        

    def has_object_permissions(self, request, view, obj):
        if (obj.sender == request.user
            or request.user.is_mediator
        ):
            return True
        elif request.method in SAFE_METHODS:
            return True
        else:
            return False

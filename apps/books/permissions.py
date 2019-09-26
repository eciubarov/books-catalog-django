from rest_framework import permissions


class IsOwnerOrReadIsAuthenticatedOnly(permissions.BasePermission):
    """
    Custom permission to only allow publisher of a book to edit and to delete it
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.publisher == request.user

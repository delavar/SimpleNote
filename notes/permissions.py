from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .models import Note

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creator of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if not isinstance(obj, Note):
            return False

        return obj.creator == request.user

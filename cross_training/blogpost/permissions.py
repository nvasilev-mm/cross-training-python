from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    # Allows only the owner to edit/delete
    def has_object_permission(self, request, view, object):
        # Safe methods include GET, HEAD & OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return object.author == request.user

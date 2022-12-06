from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwnerOrStaff(BasePermission):
    message = "Delete or edit ads can owners or admins only."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.role in [UserRoles.ADMIN]:
            return True
        return False

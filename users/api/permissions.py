from rest_framework.permissions import BasePermission, IsAdminUser, OR


class IsOwnerUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.id == obj.id)


class IsAdminUserOrIsOwnerUser(OR):
    def __init__(self):
        super().__init__(IsAdminUser(), IsOwnerUser())

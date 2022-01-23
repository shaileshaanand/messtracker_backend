from rest_framework import permissions
from core.models import User


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, User) and request.user.role == "owner"


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, User) and request.user.role == "staff"

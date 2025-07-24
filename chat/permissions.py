from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """You can update or delete your own profile, but only read another one"""

    def get_object_permission(self, request, obj, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user == request.user


class SchedulePostPermission(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.is_post or obj.user == request.user
        return obj.user == request.user

from rest_framework import permissions


class isTodayMenu(permissions.BasePermission):

    """
    Object level permission to check if menu is from today
    """

    def has_object_permission(self, request, view, obj):
        return bool(obj.isTodayMenu() or request.user.is_staff)

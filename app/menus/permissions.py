from rest_framework import permissions


class is_today_menu(permissions.BasePermission):

    """
    Object level permission to check if menu is from today
    """

    def has_object_permission(self, request, view, obj) -> bool:
        """
        [Determines if the object is today menu and or if the user is admin]
        """
        return bool(obj.is_today_menu() or request.user.is_staff)

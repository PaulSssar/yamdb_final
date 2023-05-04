from rest_framework import permissions


class IsSuperUserOrIsAdmin(permissions.BasePermission):
    """Пермишн, является ли пользователь супер юзером или админом."""

    message = 'У вас нет прав администратора или суперпользователя.'

    def has_permission(self, request, view):
        return (request.user.is_superuser or request.user.is_admin)


class IsAuthOrSuperUserOrModOrAdminOrReadOnly(permissions.BasePermission):
    """
    Пермишн, является ли пользователь
    автором/супер юзером/модератором/админом
    или только безопасные методы.
    """

    message = 'У вас нет прав доступа.'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
                )


class IsSuperUserOrIsAdminOrReadOnly(permissions.BasePermission):
    """
    Пермишн, является ли пользователь супер юзером/админом
    или только безопасные методы.
    """

    message = 'У вас нет прав доступа.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_superuser
                )

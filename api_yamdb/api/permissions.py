from rest_framework import permissions


class AdminAuthorizedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in 'GET'
            or request.user.is_authenticated and request.user.is_admin
        )


class AuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in 'GET'
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in 'GET'
            or request.user.is_authenticated and request.user.is_admin
            or request.user.is_moderator or request.user == obj.author
        )


class AdminOrUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_staff
        )


class AuthorizedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

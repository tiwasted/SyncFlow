from rest_framework import permissions


class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'employer_profile')


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'manager_profile')

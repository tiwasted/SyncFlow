from rest_framework import permissions


class CanViewOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'employer_profile'):
            # Разрешить доступ, если пользователь - работодатель этого заказа
            return obj.employer == request.user.employer_profile

        if hasattr(request.user, 'manager_profile'):
            # Менеджеры могут видеть заказы только своих работодателей
            return obj.manager == request.user.manager_profile

        if hasattr(request.user, 'employee_profile'):
            # Разрешить доступ, если пользователь - назначенный сотрудник
            return obj.assigned_employee == request.user.employee_profile

        return False


class IsEmployerOrManager(permissions.BasePermission):
    """
    Разрешение, предоставляющее доступ только пользователям с профилями employer или manager.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'employer_profile') or hasattr(request.user, 'manager_profile')

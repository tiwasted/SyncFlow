from rest_framework import permissions


class CanViewOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить доступ, если пользователь - работодатель этого заказа
        if hasattr(request.user, 'employer_profile'):
            return obj.employer == request.user.employer_profile
        # Разрешить доступ, если пользователь - назначенный сотрудник
        if hasattr(request.user, 'employee_profile'):
            return obj.assigned_employee == request.user.employee_profile
        return False
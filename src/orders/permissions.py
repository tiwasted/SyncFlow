from rest_framework import permissions
from users.models import CustomUser


class CanViewOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить доступ, если пользователь - работодатель этого заказа
        if hasattr(request.user, 'employer_profile'):
            return obj.employer == request.user.employer_profile
        # Разрешить доступ, если пользователь - назначенный сотрудник
        if hasattr(request.user, 'employee_profile'):
            return obj.assigned_employee == request.user.employee_profile
        return False


class RoleBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Определите разрешения в зависимости от роли
        if user.role == CustomUser.EMPLOYER:
            return request.method in permissions.SAFE_METHODS  # EMPLOYER может только просматривать
        elif user.role == CustomUser.EMPLOYEE:
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                return False
            return True  # EMPLOYEE может просматривать
        elif user.role == CustomUser.MANAGER:
            return True  # MANAGER может выполнять все операции

        return False

from rest_framework import generics, permissions

from employees.models import Employee
from employees.serializers.employee_serializers import EmployeeSerializer, AssigningEmployeeToOrderSerializer
from employers.permissions import IsEmployer

from orders.permissions import IsEmployerOrManager
from orders.services import OrderService


class EmployeeListView(generics.ListAPIView):
    """
    Список сотрудников для Работодателя и Менеджера
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrManager]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        profile = OrderService.get_user_profile(user)

        if hasattr(profile, 'employer_profile'):
            return Employee.objects.filter(employer=profile.employer, is_active=True)

        elif hasattr(profile, 'manager_profile'):
            return Employee.objects.filter(manager=profile.manager, is_active=True)

        return queryset.filter(is_active=True)


# Удаление сотрудников через Работодателя
class EmployeeDeleteView(generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # Деактивация сотрудника вместо его удаления
        instance.delete()


class AssigningEmployeeToOrderListView(generics.ListAPIView):
    """
    Список сотрудников для назначения на заказ для Работодателя и Менеджера (только в назначенных городах)
    """
    queryset = Employee.objects.all()
    serializer_class = AssigningEmployeeToOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrManager]

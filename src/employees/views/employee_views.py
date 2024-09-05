from rest_framework import generics, permissions

from employers.models import Employer
from employers.models import Manager
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
        # queryset = super().get_queryset()
        user = self.request.user
        profile = OrderService.get_user_profile(user)

        if isinstance(profile, Employer):
            return Employee.objects.filter(employer=profile, is_active=True)

        elif isinstance(profile, Manager):
            return Employee.objects.filter(employer=profile.employer, is_active=True)

        return Employee.objects.none()


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

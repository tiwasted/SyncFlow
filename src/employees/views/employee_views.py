from rest_framework import generics, permissions

from employees.models import Employee
from employees.serializers.employee_serializers import EmployeeSerializer, AssigningEmployeeToOrderSerializer
from employers.permissions import IsEmployer

from orders.permissions import IsEmployerOrManager
from orders.services import OrderService


# Чтение сотрудников для Работодателя
class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrManager]

    def get_view_name(self):
        user = self.request.user
        profile = OrderService.get_user_profile(user)

        if hasattr(profile, 'employer_profile'):
            return Employee.objects.filter(employer=profile.employer)

        elif hasattr(profile, 'manager_profile'):
            return Employee.objects.filter(manager=profile.manager)

        return Employee.objects.none()


# Удаление сотрудников через Работодателя
class EmployeeDeleteView(generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.delete()


class AssigningEmployeeToOrderListView(generics.ListAPIView):
    """
    Список сотрудников для назначения на заказ для Работодателя и Менеджера (только в назначенных городах)
    """
    queryset = Employee.objects.all()
    serializer_class = AssigningEmployeeToOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrManager]

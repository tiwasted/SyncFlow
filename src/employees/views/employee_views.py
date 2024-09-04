from rest_framework import generics, permissions

from employees.models import Employee
from employees.serializers.employee_serializers import EmployeeSerializer, AssigningEmployeeToOrderSerializer

from orders.permissions import IsEmployerOrManager


# Чтение сотрудников для Работодателя
class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            employer = user.employer_profile
            return Employee.objects.filter(employer=employer)
        return Employee.objects.none()


# Удаление сотрудников через Работодателя
class EmployeeDeleteView(generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
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

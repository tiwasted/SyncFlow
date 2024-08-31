from rest_framework import generics, permissions

from employees.models import Employee
from employees.serializers.employee_serializers import EmployeeSerializer, AssigningEmployeeToOrderSerializer
<<<<<<< HEAD

=======
from users.models import CustomUser
import logging
>>>>>>> origin/dev
from employees.services import RoleChecker


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


<<<<<<< HEAD
# `Список сотрудников для назначения на заказ`
=======
# Список сотрудников для назначения на заказ
>>>>>>> origin/dev
class AssigningEmployeeToOrderListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = AssigningEmployeeToOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role_checker = RoleChecker()
        user_role = role_checker.get_user_role(user)

        if user_role == 'employer':
            employer = user.employer_profile
            return Employee.objects.filter(employer=employer)
        elif user_role == 'manager':
            manager = user.manager_profile
            employer = manager.employer
            return Employee.objects.filter(employer=employer)

        return Employee.objects.none()
<<<<<<< HEAD

=======
>>>>>>> origin/dev

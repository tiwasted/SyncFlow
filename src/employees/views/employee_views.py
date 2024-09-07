from rest_framework import generics, permissions
from rest_framework.response import Response
from employees.models import Employee
from employees.serializers.employee_serializers import EmployeeSerializer
from users.models import CustomUser
import logging


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

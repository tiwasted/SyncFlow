from rest_framework import generics, permissions
from users.models import CustomUser
from employees.models import Employee
from employees.serializers.employee_serializers import EmployeeSerializer


class EmployeeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ограничьте доступ, например, только сотрудникам текущего работодателя или администраторам
        user = self.request.user
        if user.role == CustomUser.EMPLOYER:
            return Employee.objects.filter(employer=user.employer_profile)
        return Employee.objects.none()

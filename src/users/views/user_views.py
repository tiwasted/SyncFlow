from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from employers.permissions import IsEmployer
from employers.serializers.employer_serializers import EmployerInfoSerializer
from employers.serializers.manager_serializers import ManagerSerializer
from employees.serializers.employee_serializers import EmployeeIDSerializer

class UserDetailView(generics.GenericAPIView):
    """
    Представление для получения и редактирования данных любого пользователя
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            return EmployerInfoSerializer
        elif hasattr(user, 'manager_profile'):
            return ManagerSerializer
        elif hasattr(user, 'employee_profile'):
            return EmployeeIDSerializer
        raise serializers.ValidationError("Профиль не найден")

    def get_object(self):
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            return user.employer_profile
        elif hasattr(user, 'manager_profile'):
            return user.manager_profile
        elif hasattr(user, 'employee_profile'):
            return user.employee_profile
        raise serializers.ValidationError("Профиль не найден")

    def get(self, request, *args, **kwargs):
        """
        Метод для получения данных
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def put(self, request, *args, **kwargs):
        """
        Метод для редактирования данных
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

from rest_framework import generics, permissions
from users.models import CustomUser
from orders.models import Order
from employees.models import Employee
from orders.serializers.order_serializers import OrderListEmployerSerializer, FullOrderListSerializer


class OrderListEmployerView(generics.ListAPIView):
    serializer_class = OrderListEmployerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Получаем заказы только для текущего аутентифицированного работодателя
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            return Order.objects.filter(employer=user.employer_profile)
        return Order.objects.none()


class OrderListEmployeeView(generics.ListAPIView):
    serializer_class = FullOrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Получаем текущего пользователя (сотрудника)
        user = self.request.user

        try:
            employee = user.employee_profile
            return Order.objects.filter(assigned_employee=employee)
        except Employee.DoesNotExist:
            return Order.objects.none()

from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from orders.models import Order
from order_history.serializers.order_history_serializers import OrderHistorySerializer


class OrderHistoryView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'order_date', 'assigned_employee']
    ordering_fields = ['order_date', 'price', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employee_profile'):
            return Order.objects.filter(assigned_employee=user.employee_profile)
        elif hasattr(user, 'employer_profile'):
            return Order.objects.filter(employer=user.employer_profile)
        return Order.objects.none()
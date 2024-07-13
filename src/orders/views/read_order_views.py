from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from orders.serializers.read_order_serializers import OrderListEmployerSerializer


class OrderListEmployerView(generics.ListAPIView):
    serializer_class = OrderListEmployerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем заказы только для текущего аутентифицированного работодателя
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            return Order.objects.filter(employer=user.employer_profile)
        return Order.objects.none()

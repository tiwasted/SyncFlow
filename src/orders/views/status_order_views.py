from rest_framework import generics, permissions
from orders.models import Order
from orders.serializers.status_order_serializers import OrderStatusUpdateSerializer


class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

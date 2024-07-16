from rest_framework import generics, permissions
from django.utils.dateparse import parse_date
from orders.models import Order
from schedules.serializers.order_by_date_serializers import OrdersByDateSerializer


class OrdersByDateView(generics.ListAPIView):
    serializer_class = OrdersByDateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        date_str = self.request.query_params.get('date', None)
        if date_str:
            date = parse_date(date_str)
            if date:
                return Order.objects.filter(order_date=date, assigned_employee__isnull=False)
        return Order.objects.none()

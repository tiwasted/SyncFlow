from rest_framework import generics, permissions
from django.utils import timezone
from orders.models import Order
from orders.serializers.order_serializers import FullOrderListSerializer


class TodayOrdersListView(generics.ListAPIView):
    serializer_class = FullOrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()
        return Order.objects.filter(employer__user=user, order_date=today)

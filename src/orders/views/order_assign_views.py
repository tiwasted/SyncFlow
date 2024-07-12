from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.serializers.order_assign_serializers import OrderAssignEmployeeSerializer


class OrderAssignEmployeeView(generics.UpdateAPIView):
    serializer_class = OrderAssignEmployeeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            return Order.objects.filter(employer=user.employer_profile)
        return Order.objects.none()

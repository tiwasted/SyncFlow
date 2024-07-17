from rest_framework import generics, permissions
# from orders.models import Order
from orders.serializers.status_order_serializers import UpdateStatusSerializer


class BaseUpdateStatusView(generics.UpdateAPIView):
    # queryset = Order.objects.all()
    # serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        # if hasattr(user, 'employee_profile'):
            # return Order.objects.filter(assigned_employee=user.employee_profile)
        if hasattr(user, 'employer_profile'):
            return self.model.objects.filter(employer=user.employer_profile)
        return self.model.objects.none()

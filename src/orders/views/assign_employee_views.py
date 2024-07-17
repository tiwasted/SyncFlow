from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.serializers.assign_employee_serializers import AssignEmployeeToOrderSerializer


class AssignEmployeeToOrderView(generics.UpdateAPIView):
    serializer_class = AssignEmployeeToOrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            return Order.objects.filter(employer=user.employer_profile)
        return Order.objects.none()

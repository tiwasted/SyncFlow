from rest_framework import generics, permissions

# from orders.models import Order
from orders.serializers.assign_employee_serializers import AssignEmployeeToOrderSerializer


class AssignEmployeeToOrderView(generics.UpdateAPIView):
    # serializer_class = AssignEmployeeToOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            return self.model.objects.filter(employer=user.employer_profile)
        return self.model.objects.none()

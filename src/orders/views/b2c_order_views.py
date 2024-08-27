from django_filters.rest_framework import DjangoFilterBackend
from b2c_client_orders.models import B2COrder
from employers.models import EmployerCityAssignment, ManagerCityAssignment
from orders.views.base_order import BaseOrderViewSet
from orders.serializers.order_serializers import B2COrderSerializer


class B2COrderViewSet(BaseOrderViewSet):
    serializer_class = B2COrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city__name', 'order_time']

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'employer_profile'):
            employer = user.employer_profile

            employer_cities = EmployerCityAssignment.objects.filter(employer=employer).values_list('city', flat=True)

            return B2COrder.objects.filter(city__in=employer_cities)

        elif hasattr(user, 'manager_profile'):
            manager = user.manager_profile

            manager_cities = ManagerCityAssignment.objects.filter(manager=manager).values_list('city', flat=True)

            return B2COrder.objects.filter(city__in=manager_cities)

        return B2COrder.objects.none()

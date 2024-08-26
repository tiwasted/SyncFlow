from django_filters.rest_framework import DjangoFilterBackend
from b2c_client_orders.models import B2COrder
from employers.models import Employer, EmployerCityAssignment
from orders.views.base_order import BaseOrderViewSet
from orders.serializers.order_serializers import B2COrderSerializer


class B2COrderViewSet(BaseOrderViewSet):
    serializer_class = B2COrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city__name', 'order_time']

    def get_queryset(self):
        user = self.request.user
        try:
            employer = user.employer_profile

            # Получение основного города через таблицу EmployerCityAssignment
            primary_city_assignment = EmployerCityAssignment.objects.filter(
                employer=employer,
                is_primary=True
            ).first()

            if primary_city_assignment:
                primary_city = primary_city_assignment.city
                return B2COrder.objects.filter(city=primary_city)
            else:
                return B2COrder.objects.none()
        except Employer.DoesNotExist:
            return B2COrder.objects.none()

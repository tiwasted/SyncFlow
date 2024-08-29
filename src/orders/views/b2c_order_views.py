from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from b2c_client_orders.models import B2COrder
from employers.models import EmployerCityAssignment, ManagerCityAssignment
from orders.views.base_order import BaseOrderViewSet
from orders.serializers.order_serializers import B2COrderSerializer


class B2COrderViewSet(BaseOrderViewSet):
    queryset = B2COrder.objects.all()
    serializer_class = B2COrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city__id', 'order_time']

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'employer_profile'):
            employer = user.employer_profile
            # Находим освновной город работодателя
            primary_city = EmployerCityAssignment.objects.filter(employer=employer, is_primary=True).values_list('city_id', flat=True)

            # Возвращаем заказы только для основного города и со статусом 'in processing'
            return B2COrder.objects.filter(city__in=primary_city, status='in processing')

        elif hasattr(user, 'manager_profile'):
            manager = user.manager_profile

            primary_city = ManagerCityAssignment.objects.filter(manager=manager, is_primary=True).values_list('city_id', flat=True)

            # Возвращаем заказы только для основного города и со статусом 'in processing'
            return B2COrder.objects.filter(city__in=primary_city, status='in processing')

        return B2COrder.objects.none()

from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from orders.permissions import IsEmployerOrManager
from b2c_client_orders.models import B2COrder
from employers.models import Employer, Manager
from orders.models import AssignableOrderStatus
from orders.serializers.order_serializers import B2COrderSerializer
from order_history.filters import B2COrderFilter
from orders.services import OrderService


class B2COrderHistoryPagination(PageNumberPagination):
    page_size = 10  # Количество объектов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100


class B2COrderHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = B2COrder.objects.all()
    serializer_class = B2COrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = B2COrderFilter
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrManager]
    pagination_class = B2COrderHistoryPagination

    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        profile = OrderService.get_user_profile(user)

        if isinstance(profile, Employer):
            return B2COrder.objects.filter(employer=profile, status__in=[
                AssignableOrderStatus.COMPLETED,
                AssignableOrderStatus.CANCELLED
            ])

        elif isinstance(profile, Manager):
            return B2COrder.objects.filter(employer=profile.employer, status__in=[
                AssignableOrderStatus.COMPLETED,
                AssignableOrderStatus.CANCELLED
            ])

        return B2COrder.objects.none()

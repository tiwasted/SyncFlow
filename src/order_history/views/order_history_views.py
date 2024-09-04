from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from orders.permissions import IsEmployerOrManager
from b2c_client_orders.models import B2COrder
from orders.serializers.order_serializers import B2COrderSerializer
from order_history.filters import B2COrderFilter
from order_history.services import OrderFilterService


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
        return OrderFilterService.filter_orders_by_status()

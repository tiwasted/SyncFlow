from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder
from orders.serializers.order_serializers import B2BOrderSerializer, B2COrderSerializer
from order_history.filters import B2BOrderFilter, B2COrderFilter


class B2BOrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = B2BOrder.objects.all()
    serializer_class = B2BOrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = B2BOrderFilter


class B2COrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = B2COrder.objects.all()
    serializer_class = B2COrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = B2COrderFilter

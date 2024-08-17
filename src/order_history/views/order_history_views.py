from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from users.models import CustomUser
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder
from orders.serializers.order_serializers import B2BOrderSerializer, B2COrderSerializer
from order_history.filters import B2BOrderFilter, B2COrderFilter


class B2BOrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = B2BOrder.objects.all()
    serializer_class = B2BOrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = B2BOrderFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return B2BOrder.objects.filter(status__in=['completed', 'cancelled'])


class B2COrderHistoryPagination(PageNumberPagination):
    page_size = 10  # Количество объектов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100


class B2COrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = B2COrder.objects.all()
    serializer_class = B2COrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = B2COrderFilter
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = B2COrderHistoryPagination

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.EMPLOYER:
            employer = user.employer_profile
            return B2COrder.objects.filter(status__in=['completed', 'cancelled'], employer=employer)
        return B2COrder.objects.none()

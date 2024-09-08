from rest_framework import permissions

from b2c_client_orders.models import B2COrder
from orders.views.base_order import BaseOrderViewSet
from orders.serializers.order_serializers import B2COrderSerializer


class B2COrderViewSet(BaseOrderViewSet):
    queryset = B2COrder.objects.all()
    serializer_class = B2COrderSerializer
    permission_classes = [permissions.IsAuthenticated]

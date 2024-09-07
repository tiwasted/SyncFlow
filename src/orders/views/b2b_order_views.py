from b2b_client_orders.models import B2BOrder
from orders.views.base_order import BaseOrderViewSet
from orders.serializers.order_serializers import B2BOrderSerializer


class B2BOrderViewSet(BaseOrderViewSet):
    queryset = B2BOrder.objects.all()
    serializer_class = B2BOrderSerializer

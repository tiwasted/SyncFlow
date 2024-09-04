from b2c_client_orders.models import B2COrder
from orders.models import AssignableOrderStatus

class OrderFilterService:
    @staticmethod
    def filter_orders_by_status():
        """
        Фильтрует заказы по статусу COMPLETED и CANCELLED.
        """
        return B2COrder.objects.filter(status__in=[
            AssignableOrderStatus.COMPLETED,
            AssignableOrderStatus.CANCELLED
        ])

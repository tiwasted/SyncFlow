from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder
from employees.serializers.unified_order_serializers import UnifiedOrderSerializer


class AssignedOrderEmployeeListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, employee_id):
        b2b_orders = B2BOrder.objects.filter(assigned_employee_id=employee_id, status='in waiting')
        b2c_orders = B2COrder.objects.filter(assigned_employee_id=employee_id, status='in waiting')
        # Объединение заказов B2B и B2C
        orders = list(b2b_orders) + list(b2c_orders)
        # Сериализация объединенного списка заказов
        serializer = UnifiedOrderSerializer(orders, many=True)
        return Response(serializer.data)

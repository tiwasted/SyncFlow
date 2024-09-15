from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import permissions
import logging

from employees.models import Employee
from b2c_client_orders.models import B2COrder
from orders.permissions import IsEmployerOrManager
from orders.serializers.order_serializers import B2COrderSerializer

logger = logging.getLogger(__name__)


class OrderAssignmentViewSet(viewsets.GenericViewSet):
    """
    Представление для назначения сотрудников на заказ.
    """
    queryset = B2COrder.objects.all()
    serializer_class = B2COrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrManager]

    # Назначение сотрудников на заказ
    @action(detail=True, methods=['post'])
    def assign_employee(self, request, pk=None):
        order = self.get_object()
        employee_ids = request.data.get('employee_ids', [])

        if not isinstance(employee_ids, list):
            employee_ids = [employee_ids]

        if not employee_ids:
            return Response({"error": "Требуется список ID сотрудников"}, status=status.HTTP_400_BAD_REQUEST)

        # Валидация, что у заказа есть дата
        if not order.order_date:
            return Response({"error": "Невозможно назначить сотрудников на заказ без даты"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                employees = list(Employee.objects.filter(id__in=employee_ids))

                order.assign_employees(employees)

                serializer = self.get_serializer(order)
                return Response({
                    "order": serializer.data,
                    "assigned_employees": [e.id for e in employees]
                })

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Ошибка при назначении сотрудников на заказ: {order.id} {str(e)}")
            return Response({"error": "Произошла ошибка при назначении сотрудников на заказ"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

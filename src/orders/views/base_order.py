from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
import logging

from employees.models import Employee
from orders.permissions import CanViewOrder
from orders.services import OrderService

logger = logging.getLogger(__name__)


class BaseOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, CanViewOrder]

    def perform_create(self, serializer):
        OrderService.create_order(self.request.user, serializer)

    def perform_update(self, serializer):
        OrderService.update_order(self.request.user, serializer)


    # Назначение сотрудников на заказ
    @action(detail=True, methods=['post'])
    def assign_employee(self, request, pk=None):
        order = self.get_object()
        employee_ids = request.data.get('employee_ids', [])

        if not isinstance(employee_ids, list):
            employee_ids = [employee_ids]

        if not employee_ids:
            return Response({"error": "Требуется список ID сотрудников"}, status=status.HTTP_400_BAD_REQUEST)

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

    # Завершение заказа сотрудником
    @action(detail=True, methods=['post'])
    def complete_order(self, request, pk=None):
        return self._update_order_status(request, pk, 'complete')


    # Отмена заказа сотрудником
    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        return self._update_order_status(request, pk, 'cancel')

    def _update_order_status(self, request, action):
        order = self.get_object()
        try:
            employee = request.user.employee_profile
        except ObjectDoesNotExist:
            return Response({"error": "Вы не являетесь сотрудником"}, status=status.HTTP_403_FORBIDDEN)

        try:
            updated_order = OrderService.update_order_status(order, employee, action, request.data.get('report', ''))
            serializer = self.get_serializer(updated_order)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

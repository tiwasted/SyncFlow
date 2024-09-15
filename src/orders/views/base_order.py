from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from datetime import datetime
import logging

from orders.models import AssignableOrderStatus, PaymentMethod
from orders.serializers.order_serializers import B2COrderSerializer
from employees.models import Employee
from orders.permissions import CanViewOrder
from orders.services import OrderService, OrderDashboardService

logger = logging.getLogger(__name__)


class BaseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = B2COrderSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewOrder]

    def perform_create(self, serializer):
        OrderDashboardService.create_order(self.request.user, serializer)

    def perform_update(self, serializer):
        OrderDashboardService.update_order(self.request.user, serializer)


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

    # Завершение заказа сотрудником
    @action(detail=True, methods=['post'])
    def complete_order(self, request, pk=None):
        """
        Завершение заказа, проверка сотрудника, обновление статуса заказа и метода оплаты.
        """
        order = self.get_object()

        # Получаем текущего пользователя (должен быть сотрудником)
        try:
            employee = request.user.employee_profile
        except ObjectDoesNotExist:
            return Response({"error": "Вы не являетесь сотрудником"}, status=status.HTTP_403_FORBIDDEN)

        # Получаем метод оплаты из запроса
        payment_method_id = request.data.get('payment_method')
        if not payment_method_id:
            return Response({"error": "Требуется указать метод оплаты"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Проверяем наличие метода оплаты
            payment_method = PaymentMethod.objects.get(id=payment_method_id)
        except PaymentMethod.DoesNotExist:
            return Response({"error": "Недействительный метод оплаты"}, status=status.HTTP_404_NOT_FOUND)

        # Пытаемся обновить статус заказа на завершенный
        try:
            updated_order = OrderDashboardService.update_order_status(
                order, employee, 'complete', request.data.get('report', '')
            )
            updated_order.payment_method = payment_method
            updated_order.save()

            serializer = self.get_serializer(updated_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Отмена заказа сотрудником
    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        return self._update_order_status(request, pk, 'cancel')

    def _update_order_status(self, request, pk, action):
        """
        Вспомогательный метод для обновления статуса заказа.
        """
        order = self.get_object()

        # Получаем профиль сотрудника
        try:
            employee = request.user.employee_profile
        except ObjectDoesNotExist:
            return Response({"error": "Вы не являетесь сотрудником"}, status=status.HTTP_403_FORBIDDEN)

        # Пытаемся обновить статус заказа
        try:
            updated_order = OrderDashboardService.update_order_status(order, employee, action, request.data.get('report', ''))
            serializer = self.get_serializer(updated_order)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Получение завтрашних заказов по городу
    @action(detail=False, methods=['get'])
    def tomorrow_orders(self, request):
        orders = OrderDashboardService.get_tomorrow_orders(request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Получение заказов без дат
    @action(detail=False, methods=['get'])
    def orders_without_dates(self, request):
        orders = OrderDashboardService.get_orders_without_dates(request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Получение заказов по диапазону дат
    @action(detail=False, methods=['get'])
    def orders_by_dates(self, request):
        date_str = request.query_params.get('date')
        user = request.user

        # Проверка формата дат
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
        except ValueError:
            return Response({"error": "Неправильный формат даты. Используйте формат YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        primary_city = OrderService.get_primary_city(user)

        orders = OrderService.get_orders_by_date_and_time(user, date=date, city=primary_city, status=AssignableOrderStatus.IN_PROCESSING)

        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

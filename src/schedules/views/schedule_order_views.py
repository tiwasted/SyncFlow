from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

from b2c_client_orders.models import B2COrder
from employees.models import Employee
from employees.serializers.employee_serializers import ListEmployeeByOrderSerializer, SpecificEmployeeOrderSerializer
from orders.permissions import CanViewOrder
from orders.serializers.order_serializers import B2COrderSerializer
from orders.services import OrderService, OrderDashboardService
from schedules.serializers.schedule_order_serializers import  ScheduleB2COrderSerializer
from schedules.services import OrderScheduleService

import logging

logger = logging.getLogger(__name__)

class OrderScheduleViewSet(viewsets.ModelViewSet):
    queryset = B2COrder.objects.all()
    serializer_class = B2COrderSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewOrder]

    @action(detail=False, methods=['get'])
    def list_employees_by_orders(self, request):
        """
        Возвращаем список сотрудников, основанный на заказах за выбранную дату.
        """
        date = request.query_params.get('date')
        user = request.user

        if not date:
            raise ValidationError("Дата является обязательной")

        # Получаем профиль и основной город пользователя
        profile = OrderService.get_user_profile(user)
        primary_city = OrderService.get_primary_city(user)

        # Фильтруем заказы по дате и основному городу пользователя
        orders = OrderService.get_orders_by_date_and_time(date=date, city=primary_city)

        serializer = ListEmployeeByOrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_orders_for_employee(self, request):
        """
        Возвращаем список заказов для конкретного сотрудника за выбранную дату.
        """
        date = request.query_params.get('date')
        employee_id = request.query_params.get('employee_id')

        if not date:
            return Response({"detail": "Дата является обязательной"}, status=status.HTTP_400_BAD_REQUEST)

        if not employee_id:
            return Response({"detail": "ID сотрудника является обязательным"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"detail": "Сотрудник не найден"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Получаем заказы для конкретного сотрудника
            orders = OrderScheduleService.get_orders_for_employee(employee, date)
            serializer = SpecificEmployeeOrderSerializer(orders, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

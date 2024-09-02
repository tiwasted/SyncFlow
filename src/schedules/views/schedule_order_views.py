from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

from employees.models import Employee
from employees.serializers.employee_serializers import ListEmployeeByOrderSerializer, SpecificEmployeeOrderSerializer
from orders.permissions import CanViewOrder
from orders.serializers.order_serializers import B2COrderSerializer
from orders.services import OrderService, OrderDashboardService
from schedules.serializers.schedule_order_serializers import  ScheduleB2COrderSerializer
from schedules.services import OrderScheduleService

import logging

logger = logging.getLogger(__name__)

class OrderScheduleViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, CanViewOrder]

    # def list(self, request):
    #     date = request.query_params.get('date')
    #     user_id = request.query_params.get('user_id')
    #
    #     if date and user_id:
    #         try:
    #             orders = OrderScheduleService.get_orders_for_date_and_user(date, user_id)
    #             serializer = ScheduleB2COrderSerializer(orders, many=True)
    #             return Response(serializer.data)
    #         except ValidationError as e:
    #             logger.warning(f"Ошибка валидации: {str(e)}")
    #             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #         except Exception as e:
    #             logger.error(f"Произошла непредвиденная ошибка: {str(e)}")
    #             return Response({"error": "Произошла ошибка при обработке запроса"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     else:
    #         logger.warning("Дата или user_id не указаны")
    #         return Response({"error": "Дата или user_id не указаны"}, status=status.HTTP_400_BAD_REQUEST)

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

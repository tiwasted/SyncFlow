from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

from employees.serializers.employee_serializers import ListEmployeeByOrderSerializer
from orders.permissions import CanViewOrder
from orders.services import OrderService
from schedules.serializers.schedule_order_serializers import  ScheduleB2COrderSerializer
from schedules.services import OrderScheduleService

import logging

logger = logging.getLogger(__name__)

class OrderScheduleViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, CanViewOrder]

    def list(self, request):
        date = request.query_params.get('date')
        user_id = request.query_params.get('user_id')

        if date and user_id:
            try:
                orders = OrderScheduleService.get_orders_for_date_and_user(date, user_id)
                serializer = ScheduleB2COrderSerializer(orders, many=True)
                return Response(serializer.data)
            except ValidationError as e:
                logger.warning(f"Ошибка валидации: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Произошла непредвиденная ошибка: {str(e)}")
                return Response({"error": "Произошла ошибка при обработке запроса"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning("Дата или user_id не указаны")
            return Response({"error": "Дата или user_id не указаны"}, status=status.HTTP_400_BAD_REQUEST)

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

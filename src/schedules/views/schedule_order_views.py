from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
import logging

from b2c_client_orders.models import B2COrder
from employees.models import Employee
from employees.serializers.employee_serializers import ListEmployeeByOrderSerializer, SpecificEmployeeOrderSerializer
from orders.permissions import CanViewOrder, IsEmployerOrManager
from orders.serializers.order_serializers import B2COrderSerializer
from schedules.services import OrderScheduleService


logger = logging.getLogger(__name__)


class OrderScheduleViewSet(viewsets.ModelViewSet):
    queryset = B2COrder.objects.all()
    serializer_class = B2COrderSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewOrder, IsEmployerOrManager]

    @action(detail=False, methods=['get'])
    def list_employees_by_orders(self, request):
        """
        Возвращаем список сотрудников, основанный на заказах за выбранную дату.
        """
        date = request.query_params.get('date')
        user = request.user

        if not date:
            return Response({"error": "Дата является обязательной"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            orders = OrderScheduleService.get_orders_for_date_and_user(date=date, user_id=user.id)
            serializer = ListEmployeeByOrderSerializer(orders, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {str(e)}")
            return Response({"error": "Произошла неожиданная ошибка"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['get'])
    def list_orders_for_employee(self, request):
        """
        Возвращаем список заказов для конкретного сотрудника за выбранную дату.
        """
        date = request.query_params.get('date')
        employee_id = request.query_params.get('employee_id')

        logger.info(f"Полученные параметры - дата: {date}, ID сотрудника: {employee_id}")

        if not date:
            logger.error("Дата не указана")
            return Response({"detail": "Дата является обязательной"}, status=status.HTTP_400_BAD_REQUEST)

        if not employee_id:
            logger.error("ID сотрудника не указан")
            return Response({"detail": "ID сотрудника является обязательным"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            logger.error(f"Сотрудник с ID {employee_id} не найден")
            return Response({"detail": "Сотрудник не найден"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Получаем заказы для конкретного сотрудника
            logger.info(f"Получаем заказы для сотрудника {employee}")
            orders = OrderScheduleService.get_orders_for_employee(employee, date)
            serializer = SpecificEmployeeOrderSerializer(orders, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            logger.error(f"Ошибка валидации: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.critical(f"Непредвиденная ошибка: {str(e)}", exc_info=True)
            return Response({"detail": "Произошла неожиданная ошибка"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

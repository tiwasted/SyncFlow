import logging
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone

from orders.models import AssignableOrderStatus
from users.models import CustomUser
from b2c_client_orders.models import B2COrder
from employees.models import Employee
from employees.serializers.unified_order_serializers import UnifiedOrderSerializer
from orders.permissions import CanViewOrder
from orders.services import OrderService

logger = logging.getLogger(__name__)


class AssignedOrderEmployeeListView(APIView):
    permission_classes = [permissions.IsAuthenticated, CanViewOrder]

    def get(self, request):
        if request.user.role != CustomUser.EMPLOYEE:
            return Response({"detail": "Пользователь не является сотрудником."}, status=400)

        try:
            employee = OrderService.get_user_profile(request.user)
            if not isinstance(employee, Employee):
                return Response({"detail": "Профиль сотрудника не найден."}, status=400)

            logger.debug(f"Employee: {employee.id}, User: {employee.user.id}")

            if not employee.is_active:
                return Response({"detail": "Сотрудник не активен."}, status=400)

            if not employee.employer:
                return Response({"detail": "Работник не связан с работодателем."}, status=400)

        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)

        try:
            primary_city = OrderService.get_primary_city(employee)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)

        if not primary_city:
            return Response({"detail": "Основной город для работодателя этого сотрудника не найден."}, status=400)

        # Получаем дату из параметров запроса
        date_str = request.GET.get('date')
        print(f"Дата на сервере: {date_str}")

        # Фильтруем заказы по дате, если параметр присутствует
        if date_str:
            # Преобразуем строку даты в объект datetime
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            logger.debug(f"Отфильтрованная дата: {date}")

            b2c_orders = B2COrder.objects.filter(
                city=primary_city,
                assigned_employees=employee,
                status=AssignableOrderStatus.IN_WAITING,
                order_date=date
            )
        else:
            b2c_orders = B2COrder.objects.filter(
                city=primary_city,
                assigned_employee_id=employee,
                status=AssignableOrderStatus.IN_WAITING
            )

        orders = list(b2c_orders)
        # Сериализация объединенного списка заказов
        serializer = UnifiedOrderSerializer(orders, many=True)
        logger.debug(f"Сериализованные данные: {serializer.data}")
        return Response(serializer.data)

from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from django.db.models import Q
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder
from employees.serializers.unified_order_serializers import UnifiedOrderSerializer


class AssignedOrderEmployeeListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Получаем employee_id из токена JWT
        employee_id = request.user.employee_profile

        # Получаем дату из параметров запроса
        date_str = request.GET.get('date')
        print(f"Дата на сервере: {date_str}")

        # Фильтруем заказы по дате, если параметр присутствует
        if date_str:
            # Преобразуем строку даты в объект datetime
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()

            # Создаем диапазон дат для фильтрации
            start_date = timezone.make_aware(datetime.combine(date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(date, datetime.max.time()))

            date_filter = Q(order_date__range=(start_date, end_date))

            b2b_orders = B2BOrder.objects.filter(
                assigned_employee_id=employee_id,
                status='in waiting',
                order_date=date
            )
            b2c_orders = B2COrder.objects.filter(
                assigned_employee_id=employee_id,
                status='in waiting',
                order_date=date
            )
        else:
            b2b_orders = B2BOrder.objects.filter(
                assigned_employee_id=employee_id,
                status='in waiting'
            )
            b2c_orders = B2COrder.objects.filter(
                assigned_employee_id=employee_id,
                status='in waiting'
            )

        # Объединение заказов B2B и B2C
        orders = list(b2b_orders) + list(b2c_orders)
        # Сериализация объединенного списка заказов
        serializer = UnifiedOrderSerializer(orders, many=True)
        return Response(serializer.data)

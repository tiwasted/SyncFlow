from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime

from orders.serializers.order_serializers import B2COrderSerializer
from orders.models import AssignableOrderStatus
from orders.permissions import IsEmployerOrManager
from orders.services.order_dashboard_service import OrderDashboardService
from orders.services.order_service import OrderService


class BaseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = B2COrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrManager]

    def perform_create(self, serializer):
        OrderDashboardService.create_order(self.request.user, serializer)

    def perform_update(self, serializer):
        OrderService.update_order(self.request.user, serializer)

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

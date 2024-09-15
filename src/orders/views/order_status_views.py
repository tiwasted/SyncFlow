from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from b2c_client_orders.models import B2COrder
from orders.models import PaymentMethod
from orders.serializers.order_serializers import B2COrderSerializer
from orders.services.order_status_service import OrderStatusService

class OrderStatusViewSet(viewsets.GenericViewSet):
    queryset = B2COrder.objects.all()
    serializer_class = B2COrderSerializer
    permission_classes = [permissions.IsAuthenticated]

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
            updated_order = OrderStatusService.update_order_status(
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
            updated_order = OrderStatusService.update_order_status(order, employee, action, request.data.get('report', ''))
            serializer = self.get_serializer(updated_order)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

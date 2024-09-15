from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from employers.models import PaymentMethod
from employers.permissions import IsEmployer
from orders.services import OrderService
from schedules.services import CustomUser


class AddPaymentMethodView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def post(self, request, *args, **kwargs):
        """
        Добавляет способ оплаты в список доступных способов оплаты для Работодателя
        """
        employer = request.user.employer_profile
        payment_method_ids = request.data.get('payment_method_ids', [])

        if not payment_method_ids:
            return Response({"error": "Отсутствует payment_method_ids в данных запроса"}, status=status.HTTP_400_BAD_REQUEST)

        for payment_method_id in payment_method_ids:
            try:
                payment_method = PaymentMethod.objects.get(id=payment_method_id)
            except PaymentMethod.DoesNotExist:
                return Response({"error": f"Способ оплаты с ID {payment_method_id} не найден"}, status=status.HTTP_404_NOT_FOUND)

            if payment_method in employer.available_payment_methods.all():
                return Response({"error": f"Способ оплаты с ID {payment_method_id} уже добавлен"}, status=status.HTTP_400_BAD_REQUEST)

            employer.available_payment_methods.add(payment_method)

        return Response({"status": "Способ оплаты успешно добавлен"})


class AvailablePaymentMethodsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Возвращает список доступных способов оплаты для Работодателя
        """
        user = request.user

        if user.role == CustomUser.EMPLOYER:
            payment_methods = user.employer_profile.available_payment_methods.all()
        elif user.role == CustomUser.MANAGER:
            payment_methods = user.manager_profile.employer.available_payment_methods.all()
        elif user.role == CustomUser.EMPLOYEE:
            payment_methods = user.employee_profile.employer.available_payment_methods.all()
        else:
            return Response({"error": "Неизвестная роль пользователя"}, status=status.HTTP_400_BAD_REQUEST)

        # Преобразуем QuerySet в список словарей
        payment_method_data = [
            {'id': method.id, 'name': method.name}
            for method in payment_methods
        ]

        return Response({
            "payment_methods": payment_method_data
        }, status=status.HTTP_200_OK)

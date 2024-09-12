from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from employers.models import PaymentMethod
from employers.permissions import IsEmployer


class AddPaymentMethodView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def post(self, request, *args, **kwargs):
        """
        Добавляет способ оплаты в список доступных способов оплаты для Работодателя
        """
        employer = request.user.employer_profile
        payment_method_id = request.data.get('payment_method_id')

        if not payment_method_id:
            return Response({"error": "Отсутствует payment_method_id в данных запроса"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment_method = PaymentMethod.objects.get(id=payment_method_id)
        except PaymentMethod.DoesNotExist:
            return Response({"error": "Способ оплаты не найден"}, status=status.HTTP_404_NOT_FOUND)

        if payment_method in employer.available_payment_methods.all():
            return Response({"error": "Способ оплаты уже добавлен"}, status=status.HTTP_400_BAD_REQUEST)

        employer.available_payment_methods.add(payment_method)
        return Response({"status": "Способ оплаты успешно добавлен"})


class AvailablePaymentMethodsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Возвращает список доступных способов оплаты для Работодателя
        """
        employer = request.user.employer_profile
        payment_methods = employer.available_payment_methods.all()
        return Response({"payment_methods": payment_methods.values()})

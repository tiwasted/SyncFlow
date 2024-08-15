from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from b2c_client_orders.models import B2COrder, B2COrderImage


class B2COrderImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        # Получаем заказ с указанным ID
        order = get_object_or_404(B2COrder, id=order_id)
        # Находим изображение, связанные с заказом
        image = B2COrderImage.objects.filter(order=order).first()

        if image:
            return Response({"image_url": image.image.url}, status=status.HTTP_200_OK)
        return Response({"error": "Изображение не найдено"}, status=status.HTTP_404_NOT_FOUND)

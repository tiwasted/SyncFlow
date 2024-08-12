from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from b2c_client_orders.models import B2COrder, B2COrderImage
from b2c_client_orders.serializers.load_image_serializers import B2COrderImageSerializer


class AddOrderImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id, *args, **kwargs):
        try:
            order = B2COrder.objects.get(id=order_id)
        except B2COrder.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = B2COrderImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteOrderImageView(APIView):
    def delete(self, request, image_id, *args, **kwargs):
        try:
            image = B2COrderImage.objects.get(id=image_id)
        except B2COrderImage.DoesNotExist:
            return Response({'error': 'Изображение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        image.delete()
        return Response({'message': 'Изображение успешно удалено'}, status=status.HTTP_204_NO_CONTENT)

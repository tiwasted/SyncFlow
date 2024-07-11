from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.serializers.order_create_serializers import OrderCreateSerializer


class OrderCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

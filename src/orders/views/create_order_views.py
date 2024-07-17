from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.serializers.create_order_serializers import OrderCreateSerializer
from employers.models import Employer


class OrderCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():

            employer = request.user.employer_profile  # Используйте связь, указанную в related_name в модели Employer
            serializer.save(employer=employer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


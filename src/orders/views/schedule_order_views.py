from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder
from orders.serializers.order_serializers import B2BOrderSerializer, B2COrderSerializer
from orders.permissions import CanViewOrder
from django.utils.dateparse import parse_date


class OrderScheduleViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, CanViewOrder]

    def list(self, request):
        date = request.query_params.get('date')
        if date:
            try:
                date = parse_date(date)
                if not date:
                    raise ValueError("Некорректная дата")
                b2b_orders = B2BOrder.objects.filter(order_date=date, status='in waiting')
                b2c_orders = B2COrder.objects.filter(order_date=date, status='in waiting')
                b2b_serializer = B2BOrderSerializer(b2b_orders, many=True)
                b2c_seroalizer = B2COrderSerializer(b2c_orders, many=True)
                return Response(b2b_serializer.data + b2c_seroalizer.data)
            except ValueError:
                return Response({"error": "Некорректная дата"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Дата не указана"}, status=status.HTTP_400_BAD_REQUEST)

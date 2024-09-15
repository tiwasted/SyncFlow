from rest_framework import generics
from orders.models import PaymentMethod
from orders.serializers.payment_order_serializers import PaymentMethodSerializer


class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

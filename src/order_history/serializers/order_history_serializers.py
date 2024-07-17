from rest_framework import serializers
from orders.models import Order


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

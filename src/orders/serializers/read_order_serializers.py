from rest_framework import serializers
from orders.models import Order
from employees.models import Employee


class OrderListEmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_name', 'order_time', 'order_date', 'address']

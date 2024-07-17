from rest_framework import serializers
from employees.models import Employee
from orders.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_name',
                  'order_date',
                  'order_time',
                  'address',
                  'phone_number_client',
                  'first_name_client',
                  'description',
                  'price'
                  ]

    def create(self, validated_data):
        instance = Order.objects.create(**validated_data)
        return instance

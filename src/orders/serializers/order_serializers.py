# from rest_framework import serializers
# from orders.models import Order
# from employees.models import Employee
#
#
# class OrderListEmployerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['first_name_client', 'order_time', 'order_date', 'address', 'price']
#
#
# class FullOrderListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['order_name',
#                   'order_date',
#                   'order_time',
#                   'address',
#                   'phone_number_client',
#                   'first_name_client',
#                   'description',
#                   'price'
#                   ]

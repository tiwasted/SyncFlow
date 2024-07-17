# from rest_framework import serializers
# from employers.models import Employer
# from employees.models import Employee
# from orders.models import Order
#
#
# class OrderEditSerializer(serializers.ModelSerializer):
#     employer = serializers.PrimaryKeyRelatedField(queryset=Employer.objects.all(), required=False)
#     assigned_employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
#
#     class Meta:
#         model = Order
#         fields = ['employer',
#                   'order_name',
#                   'order_date',
#                   'order_time',
#                   'assigned_employee',
#                   'address',
#                   'phone_number_client',
#                   'first_name_client',
#                   'description',
#                   'price'
#                   ]
#         extra_kwargs = {
#                   'employer': {'required': False},
#                   'order_name': {'required': False},
#                   'order_date': {'required': False},
#                   'order_time': {'required': False},
#                   'assigned_employee': {'required': False},
#                   'address': {'required': False},
#                   'phone_number_client': {'required': False},
#                   'first_name_client': {'required': False},
#                   'description': {'required': False},
#                   'price': {'required': False},
#         }

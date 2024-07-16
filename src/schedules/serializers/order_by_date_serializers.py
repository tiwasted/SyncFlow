from rest_framework import serializers
from employees.models import Employee
from orders.models import Order


class EmployeeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name']


class OrdersByDateSerializer(serializers.ModelSerializer):
    assigned_employee = EmployeeInfoSerializer()

    class Meta:
        model = Order
        fields = ['address', 'price', 'assigned_employee']

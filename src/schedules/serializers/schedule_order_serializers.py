from rest_framework import serializers
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder
from employees.serializers.employee_serializers import EmployeeInfoSerializer


class ScheduleB2COrderSerializer(serializers.ModelSerializer):
    list_assigned_employees = EmployeeInfoSerializer(source='assigned_employees', many=True, read_only=True)

    class Meta:
        model = B2COrder
        fields = ['order_name', 'order_date', 'order_time', 'price','list_assigned_employees']

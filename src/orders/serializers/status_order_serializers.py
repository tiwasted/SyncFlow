from rest_framework import serializers
from orders.models import AssignableOrder
from employees.models import Employee
from employees.serializers.employee_serializers import EmployeeSerializer


class AssignableOrderSerializer(serializers.ModelSerializer):
    assigned_employee = EmployeeSerializer(read_only=True)
    assigned_employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source='assigned_employee', write_only=True, allow_null=True
    )

    class Meta:
        model = AssignableOrder
        fields = ['id', 'status', 'assigned_employee', 'assigned_employee_id']
        read_only_fields = ['id', 'assigned_employee']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if 'assigned_employee' in validated_data:
            instance.assign_employee(validated_data['assigned_employee'])
        return instance

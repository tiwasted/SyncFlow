from rest_framework import serializers

from orders.models import AssignableOrder
from users.models import CustomUser
from employers.models import Employer, Manager
from employees.models import Employee
from employees.serializers.employee_serializers import EmployeeInfoSerializer
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder


class B2BOrderSerializer(serializers.ModelSerializer):
    employer = serializers.PrimaryKeyRelatedField(read_only=True)
    # assigned_employees = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = B2BOrder
        fields = [
                  'id',
                  'employer',
                  'company_name',
                  'order_date',
                  'order_time',
                  'address',
                  'phone_number_client',
                  'name_client',
                  'price',
                  'description',
                  'created_at',
                  'status',
                  'report',
                  # 'assigned_employee',
                  # 'assigned_employee_id',
                  'assigned_employees'
                 ]

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            employer = user.employer_profile
        except Employer.DoesNotExist:
            raise serializers.ValidationError("Пользователь не связан с работодателем.")

        validated_data['employer'] = employer
        return super().create(validated_data)


class B2COrderSerializer(serializers.ModelSerializer):
    employer = serializers.PrimaryKeyRelatedField(read_only=True)
    manager = serializers.PrimaryKeyRelatedField(read_only=True)
    city = serializers.CharField(source='city.name', read_only=True)
    employee_info = EmployeeInfoSerializer(source='assigned_employees', many=True, read_only=True)
    payment_method = serializers.CharField(source='payment_method.name', read_only=True)

    class Meta:
        model = B2COrder
        fields = ['id',
                  'employer',
                  'manager',
                  'order_name',
                  'order_date',
                  'order_time',
                  'address',
                  'phone_number_client',
                  'name_client',
                  'price',
                  'description',
                  'status',
                  'report',
                  'city',
                  'payment_method',
                  'employee_info'
                  ]

    def create(self, validated_data):
        return B2COrder.objects.create(**validated_data)

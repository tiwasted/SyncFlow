from rest_framework import serializers
from employers.models import Employer
from employees.models import Employee
from employees.serializers.employee_serializers import EmployeeSerializer
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder


class B2BOrderSerializer(serializers.ModelSerializer):
    employer = serializers.PrimaryKeyRelatedField(read_only=True)
    # assigned_employee = EmployeeSerializer(read_only=True)
    # assigned_employee_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Employee.objects.all(), source='assigned_employee', write_only=True, allow_null=True
    # )

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
                  'assigned_employee',
                  'assigned_employee_id'
                 ]
        # read_only_fields = ['id', 'employer', 'assigned_employee', 'created_at']

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
    assigned_employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = B2COrder
        fields = ['id',
                  'employer',
                  'order_name',
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
                  'assigned_employee',
                  'assigned_employee_id'
                  ]

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            employer = user.employer_profile
        except Employer.DoesNotExist:
            raise serializers.ValidationError("Пользователь не связан с работодателем.")

        validated_data['employer'] = employer
        return super().create(validated_data)

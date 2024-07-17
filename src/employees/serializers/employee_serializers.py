from rest_framework import serializers
from users.models import CustomUser
from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='user.phone')

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone']

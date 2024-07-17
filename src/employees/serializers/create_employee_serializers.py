from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

from users.validators import validate_password
from employees.models import Employee

User = get_user_model()


class EmployeeCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)

    class Meta:
        model = User
        fields = ('phone', 'password', 'first_name', 'last_name')

    def validate_phone(self, value):
        # Проверка Phone
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Пользотель с таким phone уже существует")
        return value

    def create(self, validated_data):
        employer = self.context.get('employer')

        with transaction.atomic():
            user = User.objects.create_user(
                phone=validated_data['phone'],
                password=validated_data['password'],
                role='employee'
            )
            Employee.objects.create(
                user=user,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                employer=employer
            )
            return user

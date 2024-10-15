from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser
from employers.models import Manager
from employees.models import Employee
from orders.models import City


class RoleCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)
    cities = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), many=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('phone', 'password', 'first_name', 'last_name', 'role', 'cities')

    def validate(self, data):
        if data['role'] == CustomUser.MANAGER:
            if 'cities' not in data or not data['cities']:
                raise serializers.ValidationError("Менеджер должен быть привязан к городу")
        return data

    def validate_phone(self, value):
        if CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Пользователь с таким phone уже существует")
        return value

    def create(self, validated_data):
        employer = self.context.get('employer')
        role = validated_data.pop('role')
        cities = validated_data.pop('cities', None)

        with transaction.atomic():
            user = CustomUser.objects.create_user(
                phone=validated_data['phone'],
                password=validated_data['password'],
                role=role
            )

            if role == CustomUser.EMPLOYEE:
                Employee.objects.create(
                    user=user,
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    employer=employer
                )
            elif role == CustomUser.MANAGER:
                manager = Manager.objects.create(
                    user=user,
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    employer=employer
                )
                if cities:
                    manager.cities.set(cities)

            return user

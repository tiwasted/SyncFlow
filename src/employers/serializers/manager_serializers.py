from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

from users.validators import validate_password
from users.models import CustomUser
from employers.models import Manager

User = get_user_model()


# Сериализатор для создания менеджеров
class ManagerCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone', 'password', 'first_name', 'last_name', 'role')

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
                role='manager'
            )
            Manager.objects.create(
                user=user,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                employer=employer
            )
            return user


# Сериализатор для менеджеров
class ManagerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Manager
        fields = ['id', 'phone', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        # Обновляем данные менеджера
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Обновляем номер телефона пользователя
        user_data = validated_data.get('user', {})
        phone = user_data.get('phone')
        if phone:
            # Проверяем, что номер телефона уникален
            if CustomUser.objects.filter(phone=phone).exclude(id=instance.user.id).exists():
                raise serializers.ValidationError({"phone": "Этот номер телефона уже используется."})

            instance.user.phone = phone
            instance.user.save()

        instance.save()
        return instance

    # def get_role(self, obj):
    #     return obj.user.role

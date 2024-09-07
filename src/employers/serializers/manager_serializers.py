from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

from orders.serializers.city_order_serializers import CitySerializer, CityInfoSerializer
from users.validators import validate_password
from users.models import CustomUser
from employers.models import Manager
from orders.models import City

User = get_user_model()


class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manager
        fields = ['id', 'first_name', 'last_name']


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


class ManagerInfoSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='user.phone')
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Manager
        fields = ['id', 'phone', 'first_name', 'last_name', 'cities']


class ManagerSerializerUpdate(serializers.ModelSerializer):
    """
    Сериализатор для обновления данных менеджера
    """
    phone = serializers.CharField(write_only=True, required=False)
    cities = CityInfoSerializer(many=True, read_only=True)
    add_cities = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    remove_cities = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Manager
        fields = ['id', 'phone', 'first_name', 'last_name', 'cities', 'add_cities', 'remove_cities']

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

        # Добавляем новые города
        add_cities = validated_data.get('add_cities', [])
        for city_id in add_cities:
            try:
                city = City.objects.get(id=city_id)
                instance.cities.add(city)
            except City.DoesNotExist:
                raise serializers.ValidationError(f"Город с id {city_id} не существует.")

        # Удаляем города
        remove_cities = validated_data.get('remove_cities', [])
        for city_id in remove_cities:
            try:
                city = City.objects.get(id=city_id)
                instance.cities.remove(city)
            except City.DoesNotExist:
                raise serializers.ValidationError(f"Город с id {city_id} не существует.")

        instance.save()
        return instance

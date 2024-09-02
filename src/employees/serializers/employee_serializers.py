from rest_framework import serializers

from b2c_client_orders.models import B2COrder
from users.models import CustomUser
from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='user.phone')

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'phone']

    # Обновление пароля
    def update(self, instance, validated_data):
        # Обновляем данные сотрудника
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


class AssignedEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name']


class EmployeeInfoSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='user.phone')

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone']


class AssigningEmployeeToOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name']


class ListEmployeeByOrderSerializer(serializers.ModelSerializer):
    """Serializer для списка сотрудников, основанный на заказах за выбранную дату."""
    employees = AssignedEmployeeSerializer(source='assigned_employees', many=True, read_only=True)

    class Meta:
        model = B2COrder
        fields = ['order_name','order_time','employees']

    def get_employees(self, obj):
        """
        Получение списка сотрудников для данного заказа.
        """
        return obj.assigned_employees.all()


class SpecificEmployeeOrderSerializer(serializers.ModelSerializer):
    """Serializer для списка заказов для конкретного сотрудника."""

    class Meta:
        model = B2COrder
        fields = ['order_name', 'order_date', 'order_time', 'address', 'price']

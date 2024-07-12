from rest_framework import serializers
from orders.models import Order
from employees.models import Employee


class OrderAssignEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['assigned_employee']

    def validate_assigned_employee(self, value):
        request = self.context.get('request')
        user = request.user
        if not hasattr(user, 'employer_profile'):
            raise serializers.ValidationError("У пользователя нет профиля Работодателя")

        employer = user.employer_profile
        if value not in Employee.objects.filter(employer=employer):
            raise serializers.ValidationError("Работник не принадлежит этому Работадателю")

        return value

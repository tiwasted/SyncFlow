from rest_framework import serializers
from orders.models import Order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def update_status(self, value):
        if value not in ['completed', 'cancelled']:
            raise serializers.ValidationError("Неверный статус")
        return value

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        if status == 'completed':
            instance.complete_order()
        elif status == 'cancelled':
            instance.cancel_order()
        return instance

from rest_framework import serializers
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder


class UnifiedOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_type = serializers.SerializerMethodField()
    company_name = serializers.CharField(required=False)
    order_name = serializers.CharField(required=False)
    order_date = serializers.DateField()
    order_time = serializers.TimeField()
    address = serializers.CharField()
    phone_number_client = serializers.CharField(max_length=11)
    name_client = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    status = serializers.CharField()
    assigned_employee_id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField()

    def get_order_type(self, instance):
        if isinstance(instance, B2BOrder):
            return 'B2B'
        elif isinstance(instance, B2COrder):
            return 'B2C'
        return 'Unknown'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(instance, B2BOrder):
            representation['order_type'] = 'B2B'
            representation['company_name'] = instance.company_name
        elif isinstance(instance, B2COrder):
            representation['order_type'] = 'B2C'
            representation['order_name'] = instance.order_name
        return representation

from rest_framework import serializers
from schedules.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    order_date = serializers.SerializerMethodField()
    order_time = serializers.SerializerMethodField()
    order_type = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['b2b_order', 'b2c_order', 'employee', 'order_date', 'order_time', 'order_type']

    def get_order_date(self, obj):
        return obj.b2b_order.order_date if obj.b2b_order else obj.b2c_order.order_date

    def get_order_time(self, obj):
        return obj.b2b_order.order_time if obj.b2b_order else obj.b2c_order.order_time

    def get_order_type(self, obj):
        return 'B2B' if obj.b2b_order else 'B2C'

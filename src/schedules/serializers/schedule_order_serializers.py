from rest_framework import serializers
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder



class ScheduleB2COrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = B2COrder
        fields = ['order_name', 'order_date', 'order_time', 'status']

from rest_framework import serializers
from b2c_client_orders.models import B2COrder, B2COrderImage


class B2COrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2COrderImage
        fields = ('image')

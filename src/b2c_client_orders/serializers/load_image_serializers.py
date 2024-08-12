from rest_framework import serializers
from b2c_client_orders.models import B2COrder, B2COrderImage


class B2COrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2COrderImage
        fields = ('id', 'image', 'uploaded_at')


class B2COrderSerializer(serializers.ModelSerializer):
    images = B2COrderImageSerializer(many=True, read_only=True)

    class Meta:
        model = B2COrder
        fields = '__all__'

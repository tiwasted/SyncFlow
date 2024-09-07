from rest_framework import serializers


class SetPrimaryCitySerializer(serializers.Serializer):
    city_id = serializers.IntegerField()

    class Meta:
        fields = ['city_id']

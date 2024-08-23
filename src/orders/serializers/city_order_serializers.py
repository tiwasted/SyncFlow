from rest_framework import serializers
from orders.models import Country, City


class CitySerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = City
        fields = ['id', 'name', 'country']


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'cities']

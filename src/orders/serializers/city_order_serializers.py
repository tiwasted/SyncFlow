from rest_framework import serializers
from orders.models import Country, City


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'name', 'country']


class CityInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'name']

class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'cities']

from rest_framework import serializers
from employers.models import Employer
from orders.serializers.city_order_serializers import CountrySerializer, CitySerializer


class EmployerSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Employer
        fields = ['user', 'company_name', 'company_description', 'countries', 'cities']


class EmployerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['first_name', 'last_name', 'company_name', 'company_description']

from rest_framework import serializers
from orders.models import Country, City


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'name', 'country']


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'cities']


class CountryWithCitiesSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['id', 'name', 'cities']

    def get_cities(self, obj):
        # Возвращаем только города, которые выбраны пользователем
        user_cities = self.context['request'].user.employer_profile.selected_cities.all()
        return CitySerializer(user_cities.filter(country=obj), many=True).data

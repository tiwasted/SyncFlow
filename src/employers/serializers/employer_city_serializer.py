from rest_framework import serializers
# from employers.models import EmployerCity


# class EmployerCitySerializer(serializers.ModelSerializer):
#     city_name = serializers.CharField(source='city.name', read_only=True)
#     country_name = serializers.CharField(source='city.country.name', read_only=True)
#
#     class Meta:
#         model = EmployerCity
#         fields = ['id', 'city_name', 'country_name']


class SetPrimaryCitySerializer(serializers.Serializer):
    city_id = serializers.IntegerField()

    class Meta:
        fields = ['city_id']

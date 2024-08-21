from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.models import Country, City
from orders.serializers.city_order_serializers import CountrySerializer, CitySerializer


class CountryListView(APIView):
    def get(self, request, *args, **kwargs):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            country = Country.objects.get(pk=kwargs['pk'])
        except Country.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Убедитесь, что удаление не нарушает целостность данных
        if City.objects.filter(country=country).exists():
            return Response(
                {'detail': 'Не удается удалить страну с привязанными к ней городами.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CityListView(APIView):
    def get(self, request, *args, **kwargs):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            city = City.objects.get(pk=kwargs['pk'])
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

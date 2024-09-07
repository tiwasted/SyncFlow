from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from orders.models import Country, City
from orders.serializers.city_order_serializers import CountrySerializer, CitySerializer

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CitiesByCountryView(ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        country_id = self.kwargs['country_id']
        return City.objects.filter(country_id=country_id)

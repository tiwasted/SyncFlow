from rest_framework import status, permissions, generics
from rest_framework.response import Response

from employers.models import EmployerCityAssignment
from orders.models import Country, City
from orders.serializers.city_order_serializers import CountryWithCitiesSerializer


class AddCountriesView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        employer = request.user.employer_profile
        country_ids = request.data.get('country_ids', [])
        countries = Country.objects.filter(id__in=country_ids)
        employer.selected_countries.add(*countries)
        return Response({"status": "Страна или страны успешно добавлены"})

class AddCitiesView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        employer = request.user.employer_profile
        city_ids = request.data.get('city_ids', [])
        cities = City.objects.filter(id__in=city_ids)

        selected_countries = employer.selected_countries.all()
        if not cities.filter(country__in=selected_countries).exists():
            return Response({"status": "Некоторые города не относятся к выбранным странам"}, status=status.HTTP_400_BAD_REQUEST)

        # Добавление городов
        employer.selected_cities.add(*cities)

        # Создание связей в EmployerCityAssignment
        for city in cities:
            EmployerCityAssignment.objects.get_or_create(employer=employer, city=city)

        return Response({"status": "Город или города успешно добавлены"})


class AddedCountriesWithCitiesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountryWithCitiesSerializer

    def get(self, request, *args, **kwargs):
        employer = request.user.employer_profile
        # Получите страны, которые выбрал пользователь
        selected_countries = employer.selected_countries.prefetch_related('cities')
        # Передаем контекст в сериализатор
        serializer = self.get_serializer(selected_countries, many=True, context={'request': request})
        return Response(serializer.data)

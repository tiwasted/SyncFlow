from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from rest_framework.response import Response

from employers.permissions import IsEmployer
from orders.permissions import IsEmployerOrManager
from users.models import CustomUser
from employers.models import EmployerCityAssignment, Employer, Manager
from orders.models import Country, City
from orders.serializers.city_order_serializers import CitySerializer


class AddCountriesView(generics.UpdateAPIView):
    """
    Добавление стран в список выбранных стран работодателя
    """
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def post(self, request, *args, **kwargs):
        employer = request.user.employer_profile
        country_ids = request.data.get('country_ids', [])
        countries = Country.objects.filter(id__in=country_ids)
        employer.selected_countries.add(*countries)
        return Response({"status": "Страна или страны успешно добавлены"})


class AddCitiesView(generics.UpdateAPIView):
    """
    Добавление городов в список выбранных городов работодателя
    """
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def post(self, request, *args, **kwargs):
        employer = request.user.employer_profile
        city_ids = request.data.get('city_ids', [])
        cities = City.objects.filter(id__in=city_ids)

        selected_countries = employer.selected_countries.all()
        if not cities.filter(country__in=selected_countries).exists():
            return Response({"status": "Некоторые города не относятся к выбранным странам"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, какие из этих городов уже добавлены
        already_added_cities = employer.selected_cities.filter(id__in=city_ids)

        if already_added_cities.exists():
            already_added_city_names = ", ".join(already_added_cities.values_list('name', flat=True))
            return Response(
            {"status": f"Города {already_added_city_names} уже добавлены"},
                  status=status.HTTP_400_BAD_REQUEST
            )

        # Добавление городов
        employer.selected_cities.add(*cities)

        # Создание связей в EmployerCityAssignment
        for city in cities:
            EmployerCityAssignment.objects.get_or_create(employer=employer, city=city)

        return Response({"status": "Город или города успешно добавлены"})


class AvailableCitiesView(APIView):
    """
    Возвращает список доступных городов для пользователей
    """
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrManager]

    def get(self, request, *args, **kwargs):
        user = request.user
        cities = []

        if user.role == CustomUser.EMPLOYER:
            employer = user.employer_profile
            cities = employer.selected_cities.all()
        elif user.role == CustomUser.MANAGER:
            employer = user.manager_profile
            cities = employer.cities.all()

        city_data = [{'id': city.id, 'name': city.name} for city in cities]

        return Response({
            "cities": city_data
        }, status=status.HTTP_200_OK)


# Отображение городов Employer и Manager
class ListCitiesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitySerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == CustomUser.EMPLOYER:
            try:
                employer = user.employer_profile
                return employer.selected_cities.all()
            except Employer.DoesNotExist:
                return City.objects.none()

        elif user.role == CustomUser.MANAGER:
            try:
                manager = user.manager_profile
                return manager.cities.all()
            except Manager.DoesNotExist:
                return City.objects.none()

        else:
            return City.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        role = "unknown"
        if request.user.role == CustomUser.EMPLOYER:
            role = "employer"
        elif request.user.role == CustomUser.MANAGER:
            role = "manager"

        return Response({
            "role": role,
            "cities": serializer.data
        })

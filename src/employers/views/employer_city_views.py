from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from django.db.models import Q

from users.models import CustomUser
from employers.models import EmployerCityAssignment, ManagerCityAssignment, Employer, Manager
from orders.models import Country, City
from orders.serializers.city_order_serializers import CountryWithCitiesSerializer, CitySerializer


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


class AvailableCitiesView(APIView):

    def get(self, request, *args, **kwargs):
        employer = request.user.employer_profile
        cities = employer.selected_cities.all()
        city_data = [{'id': city.id, 'name': city.name} for city in cities]

        return Response({
            "cities": city_data
        }, status=status.HTTP_200_OK)


class CityService:
    @staticmethod
    def get_cities_for_employer(employer):
        employer_cities = employer.selected_cities.values_list('id', flat=True)

        manager_cities = City.objects.filter(
            employercityassignments__employer=employer
        ).values_list('id', flat=True).distinct()

        return City.objects.filter(id__in=set(employer_cities) | set(manager_cities))

    @staticmethod
    def get_cities_for_manager(manager):
        employer_cities = manager.employer.selected_cities.values_list('id', flat=True)

        manager_cities_ids = ManagerCityAssignment.objects.filter(
            manager=manager
        ).values_list('city_id', flat=True)

        return City.objects.filter(id__in=set(employer_cities) | set(manager_cities_ids))


# class AddedCountriesWithCitiesView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CountryWithCitiesSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#
#         if user.role == CustomUser.EMPLOYER:
#             try:
#                 employer = user.employer_profile
#                 all_cities = CityService.get_cities_for_employer(employer)
#             except Employer.DoesNotExist:
#                 return Response({"error": "У этого пользователя нет профиля Employer."},
#                                 status=status.HTTP_404_NOT_FOUND)
#
#         elif user.role == CustomUser.MANAGER:
#             try:
#                 manager = user.manager_profile
#                 all_cities = CityService.get_cities_for_manager(manager)
#             except Manager.DoesNotExist:
#                 return Response({"error": "У этого пользователя нет профиля Manager."},
#                                 status=status.HTTP_404_NOT_FOUND)
#
#         else:
#             return Response({"error": "Пользователь не является ни Employer, ни Manager."},
#                             status=status.HTTP_403_FORBIDDEN)
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)

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



        # # Получаем страны, связанные с этими городами
        # selected_countries = Country.objects.filter(cities__in=all_cities).distinct().prefetch_related('cities')
        #
        # # Передаем контекст в сериализатор
        # serializer = self.get_serializer(selected_countries, many=True, context={'request': request})
        # return Response(serializer.data)


# class AddedCountriesWithCitiesView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CountryWithCitiesSerializer
#
#     def get(self, request, *args, **kwargs):
#         employer = request.user.employer_profile
#         # Получите страны, которые выбрал пользователь
#         selected_countries = employer.selected_countries.prefetch_related('cities')
#         # Передаем контекст в сериализатор
#         serializer = self.get_serializer(selected_countries, many=True, context={'request': request})
#         return Response(serializer.data)



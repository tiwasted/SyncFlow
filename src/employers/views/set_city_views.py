from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# from orders.models import City
from employers.models import EmployerCityAssignment


# API для выбора основного города
class SetPrimaryCityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        city_id = request.data.get('city_id')
        employer = request.user.employer_profile

        # Убираем статус основного города у всех записей
        employer.city_assignments.update(is_primary=False)

        # Устанавливаем выбранный город как основной
        assignment = get_object_or_404(EmployerCityAssignment, employer=employer, city_id=city_id)
        assignment.is_primary = True
        assignment.save()

        return Response({"status": "Основной город успешно изменен."}, status=status.HTTP_200_OK)


# API для получения основного города
class GetPrimaryCityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        employer = request.user.employer_profile
        primary_city = employer.city_assignments.filter(is_primary=True).first()

        if primary_city:
            data = {
                "city_id": primary_city.city.id,
                "city_name": primary_city.city.name,
                "country": primary_city.city.country.name
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Основной город не назначен."}, status=status.HTTP_404_NOT_FOUND)

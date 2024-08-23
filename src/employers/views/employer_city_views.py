from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from employers.models import Employer, EmployerCity
from employers.serializers.employer_city_serializer import EmployerCitySerializer
from orders.models import City


class EmployerCitiesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            employer = Employer.objects.get(user=request.user)
        except Employer.DoesNotExist:
            return Response(status=404)

        cities = EmployerCity.objects.filter(employer=employer)
        serializer = EmployerCitySerializer(cities, many=True)
        return Response(serializer.data)


class EmployerCityManagementView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            employer = Employer.objects.get(user=request.user)
        except Employer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        city_id = request.data.get('city_id')
        if not city_id:
            return Response({"detail": "Требуется ID города"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return Response({"detail": "Город не найден"}, status=status.HTTP_404_NOT_FOUND)

        EmployerCity.objects.get_or_create(employer=employer, city=city)
        return Response({"detail": "Город успешно добавлен."}, status=status.HTTP_201_CREATED)

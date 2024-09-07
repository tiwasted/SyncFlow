from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from employers.models import Employer
from employers.serializers.employer_serializers import EmployerSerializer
from orders.models import Country, City


class EmployerView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            employer = Employer.objects.get(user=request.user)
        except Employer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployerSerializer(employer)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        employer = Employer.objects.get(user=request.user)
        country_ids = request.data.get('countries', [])
        city_ids = request.data.get('cities', [])

        # Обновляем связи
        employer.countries.set(Country.objects.filter(id__in=country_ids))
        employer.cities.set(City.objects.filter(id__in=city_ids))

        serializer = EmployerSerializer(employer)
        return Response(serializer.data)

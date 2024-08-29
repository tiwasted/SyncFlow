from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from employers.models import ManagerCityAssignment
from users.models import CustomUser
from orders.models import City
from employers.serializers.role_serializers import RoleCreateSerializer


class RoleListView(APIView):
    def get(self, *args, **kwargs):
        roles = [role for role in CustomUser.ROLE_CHOICES if role[0] != CustomUser.EMPLOYER]

        return Response({
            "roles": roles
        }, status=status.HTTP_200_OK)


class RoleCreateView(APIView):
    serializer_class = RoleCreateSerializer

    def post(self, request):
        serializer = RoleCreateSerializer(data=request.data, context={'employer': request.user.employer_profile})

        if serializer.is_valid():
            # Create the Manager (profile) user
            user = serializer.save()

            city_ids = request.data.get('city_ids', [])
            if city_ids:
                cities = City.objects.filter(id__in=city_ids)

                selected_countries = user.employer_profile.selected_countries.all()
                if not cities.filter(country__in=selected_countries).exists():
                    return Response({"status": "Некоторые города не относятся к выбранным странам"},
                                    status=status.HTTP_400_BAD_REQUEST)

                for city in cities:
                    ManagerCityAssignment.manager_city_assignment.get_or_create(manager=user.manager_profile, city=city)

            return Response({
                "message": "Пользователь успешно создан",
                "user_id": user.id,
                "role": user.role},
                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

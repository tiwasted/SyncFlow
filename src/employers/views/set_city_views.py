from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from employers.models import EmployerCityAssignment, ManagerCityAssignment
from employers.serializers.employer_city_serializer import SetPrimaryCitySerializer
from orders.permissions import IsEmployerOrManager

from orders.services import OrderService


# API для выбора основного города
class SetPrimaryCityView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrManager]
    serializer_class = SetPrimaryCitySerializer

    def post(self, request, *args, **kwargs):
        city_id = request.data.get('city_id')
        user = request.user

        if not city_id:
            return Response({"error": "Необходимо указать ID города."},
                            status=status.HTTP_400_BAD)

        if user.role == 'employer':
            employer = user.employer_profile
            # Убираем статус основного города у всех записей
            employer.city_assignments.update(is_primary=False)
            # Устанавливаем выбранный город как основной
            assignment, created = EmployerCityAssignment.objects.get_or_create(employer=employer, city_id=city_id)
            assignment.is_primary = True
            assignment.save()
        elif user.role == 'manager':
            manager = user.manager_profile
            # Убираем статус основного города у всех записей
            manager.city_assignments.update(is_primary=False)
            # Устанавливаем выбранный город как основной
            assignment, created = ManagerCityAssignment.objects.get_or_create(manager=manager, city_id=city_id)
            assignment.is_primary = True
            assignment.save()
        else:
            return Response({"error": "Недопустимая роль пользователя."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "Основной город успешно изменен."}, status=status.HTTP_200_OK)


# API для получения основного города
class GetPrimaryCityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = OrderService.get_user_profile(request.user)

        if hasattr(profile, 'city_assignments'):
            primary_city = profile.city_assignments.filter(is_primary=True).first()

            if primary_city:
                data = {
                    "city_id": primary_city.city.id,
                    "city_name": primary_city.city.name,
                    "country": primary_city.city.country.name
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Основной город не назначен."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from employers.models import Manager, ManagerCityAssignment
from orders.models import City
from orders.serializers.city_order_serializers import CitySerializer


# Назначение города менеджеру
class AssignCityToManagerView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Только аутентифицированные пользователи

    def post(self, request, manager_id):
        if request.user.role != 'employer':
            return Response(data={"error": "Только Employer может назначать города менеджерам."}, status=status.HTTP_403_FORBIDDEN)

        manager = get_object_or_404(Manager, id=manager_id)
        city_id = request.data.get('city_id')
        city = get_object_or_404(City, id=city_id)

        if city not in manager.employer.selected_cities.all():
            return Response(data={"error": "Этот город недоступен для данного менеджера"}, status=status.HTTP_400_BAD_REQUEST)

        ManagerCityAssignment.objects.update_or_create(manager=manager, city=city)

        return Response(data={"success": "Город успешно привязан к менеджеру"}, status=status.HTTP_200_OK)


# Получение городов менеджера
class ManagerCitiesView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Только аутентифицированные пользователи

    def get(self, request, manager_id):
        manager = get_object_or_404(Manager, id=manager_id)

        # Проверяем, что текущий пользователь является этим менеджером
        if request.user != manager.user:
            return Response({"error": "Вы не можете просматривать города другого менеджера"}, status=status.HTTP_403_FORBIDDEN)

        # Получаем города, доступные работодателю менеджера
        assigned_cities = manager.city_assignments.all()

        # Сериализуем города и возвращаем ответ
        serializer = CitySerializer([assigment.city for assigment in assigned_cities], many=True)
        return Response(serializer.data)

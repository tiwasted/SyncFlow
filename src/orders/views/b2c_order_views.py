from django_filters.rest_framework import DjangoFilterBackend
from b2c_client_orders.models import B2COrder
from employers.models import Employer, EmployerCityAssignment
from orders.models import City
from orders.views.base_order import BaseOrderViewSet
from orders.serializers.order_serializers import B2COrderSerializer


class B2COrderViewSet(BaseOrderViewSet):
    serializer_class = B2COrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city__name', 'order_time']

    def get_queryset(self):
        user = self.request.user
        try:
            employer = user.employer_profile

            # Получение основного города через таблицу EmployerCityAssignment
            primary_city_assignment = EmployerCityAssignment.objects.filter(
                employer=employer,
                is_primary=True
            ).first()

            if primary_city_assignment:
                primary_city = primary_city_assignment.city
                return B2COrder.objects.filter(city=primary_city)
            else:
                return B2COrder.objects.none()
        except Employer.DoesNotExist:
            return B2COrder.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        employer = user.employer_profile

        # Получаем основной город из EmployerCityAssignment
        primary_city_assignment = EmployerCityAssignment.objects.filter(
            employer=employer,
            is_primary=True
        ).first()

        if primary_city_assignment:
            city = primary_city_assignment.city
            serializer.save(city=city, employer=employer)
        else:
            serializer.save(employer=employer)

    # def get_queryset(self):
    #     employer = self.request.user.employer_profile
    #     return self.queryset.filter(employer=employer)
    #
    # def perform_create(self, serializer):
    #     selected_city_id = self.request.data.get('city_id')
    #     employer = self.request.user.employer_profile
    #
    #     if not selected_city_id:
    #         # Если город не выбран, используем основной город
    #         primary_city = employer.city_assignments.filter(is_primary=True).first()
    #         if primary_city:
    #             selected_city_id = primary_city.city.id
    #
    #     city = City.objects.get(id=selected_city_id) if selected_city_id else None
    #     serializer.save(city=city, employer=employer)

    # def get_queryset(self):
    #     employer = self.request.user.employer_profile
    #
    #     # Получаем все города, добавленные пользователем
    #     selected_cities = employer.selected_cities.all()
    #
    #     # Фильтруем заказы по этим городам
    #     queryset = B2COrder.objects.filter(city__in=selected_cities)
    #
    #     # Дополнительно можно фильтровать по конкретному городу, если передан параметр 'city_id'
    #     city_id = self.request.query_params.get('city_id')
    #     if city_id:
    #         queryset = queryset.filter(city_id=city_id)
    #
    #     return queryset
    #
    # def perform_create(self, serializer):
    #     selected_city_id = self.request.session.get('selected_city_id')
    #     employer = self.request.user.employer_profile
    #
    #     # Сначала сохраняем заказ, чтобы он получил ID
    #     order = serializer.save(employer=employer)
    #
    #     if selected_city_id:
    #         city = City.objects.get(id=selected_city_id)
    #         order.city = city
    #         order.save(update_fields=['city'])

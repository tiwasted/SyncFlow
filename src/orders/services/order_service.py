from django.core.exceptions import ValidationError

import logging

from b2c_client_orders.models import B2COrder
from employees.models import Employee
from employers.models import Employer, EmployerCityAssignment, Manager, ManagerCityAssignment
from users.models import CustomUser

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OrderService:
    """Бизнес-логика для работы с заказами."""

    @staticmethod
    def get_user_profile(user):
        """
        Возвращает профиль пользователя, если у него есть роль employer или manager.
        """
        logger.debug(f"Получение профиля пользователя: {user.id}, роль: {user.role}")

        if user.role == CustomUser.EMPLOYER:
            try:
                return user.employer_profile
            except Employer.DoesNotExist:
                logger.warning(f"Работодатель не найден для пользователя: {user.id}")
                raise ValidationError("Работодатель не найден для пользователя")
        elif user.role == CustomUser.MANAGER:
            try:
                return user.manager_profile
            except Manager.DoesNotExist:
                logger.warning(f"Менеджер не найден для пользователя: {user.id}")
                raise ValidationError("Менеджер не найден для пользователя")
        elif user.role == CustomUser.EMPLOYEE:
            try:
                return user.employee_profile
            except Employee.DoesNotExist:
                logger.warning(f"Сотрудник не найден для пользователя: {user.id}")
                raise ValidationError("Сотрудник не найден для пользователя")

        raise ValidationError(
            f"Профиль пользователя (ID: {user.id}) не является работодателем, менеджером или сотрудником")

    @staticmethod
    def get_primary_city(user_or_profile):
        """
        Получение основного города пользователя.
        """
        logger.debug("Получение основного города для пользователя: %s", user_or_profile)

        if isinstance(user_or_profile, CustomUser):
            profile = OrderService.get_user_profile(user_or_profile)
        else:
            profile = user_or_profile

        if isinstance(profile, Employer):
            primary_city_assignment = EmployerCityAssignment.objects.filter(
                employer=profile,
                is_primary=True
            ).first()
        elif isinstance(profile, Manager):
            primary_city_assignment = ManagerCityAssignment.objects.filter(
                manager=profile,
                is_primary=True
            ).first()
        elif isinstance(profile, Employee):
            employer = profile.employer
            if not employer:
                logger.warning("Сотрудник %s не связан с работодателем", profile)
                raise ValidationError("Сотрудник не связан с работодателем")
            primary_city_assignment = EmployerCityAssignment.objects.filter(
                employer=employer,
                is_primary=True
            ).first()
        else:
            logger.warning("Профиль %s не является допустимым типом", profile)
            raise ValidationError("Профиль пользователя не является работодателем, менеджером или сотрудником")

        if not primary_city_assignment:
            logger.warning("Основной город не найден для профиля %s", profile)
            raise ValidationError(f"Основной город не найден для профиля {profile}")

        return primary_city_assignment.city if primary_city_assignment else None

    @staticmethod
    def update_order(user, serializer):
        """
        Редактирование заказа в зависимости от роли пользователя (менеджер или работодатель).
        """
        logger.debug("Обновление заказа для пользователя: %s", user)
        if hasattr(user, 'manager_profile'):
            manager = user.manager_profile
            return serializer.save(manager=manager, employer=manager.employer)
        elif hasattr(user, 'employer_profile'):
            employer = user.employer_profile
            return serializer.save(employer=employer)
        else:
            return serializer.save()

    @staticmethod
    def get_orders_by_date_and_time(user, date=None, city=None, status=None):
        """
        Получение заказов по выбранной дате, отсортированных по времени.
        """
        logger.debug("Получение заказов по дате: %s, городу: %s, статусу: %s", date, city, status)
        primary_city = OrderService.get_primary_city(user)

        if user.role == 'employer':
            employer = user.employer_profile
        elif user.role == 'manager':
            employer = user.manager_profile.employer
        else:
            return B2COrder.objects.none()

        # Фильтруем заказы по работодателю
        queryset = B2COrder.objects.filter(employer=employer)

        if date:
            queryset = queryset.filter(order_date=date)

        if city:
            queryset = queryset.filter(city=city)
        elif primary_city:
            queryset = queryset.filter(city=primary_city)

        if status:
            queryset = queryset.filter(status=status)

        queryset = queryset.order_by('order_time')
        logger.info("Получено заказов: %s", queryset)

        return queryset

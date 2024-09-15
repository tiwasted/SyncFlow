from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from django.db.models import Q
import logging

from b2c_client_orders.models import B2COrder
from orders.models import AssignableOrderStatus
from orders.services.order_service import OrderService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OrderDashboardService:
    """Бизнес-логика для работы с заказами во вкладке Dashboard."""

    @staticmethod
    def create_order(user, serializer):
        """
        Создание заказа.
        """
        logger.debug("Создание заказа для пользователя: %s", user)
        primary_city = OrderService.get_primary_city(user)

        if hasattr(user, 'manager_profile'):
            manager = user.manager_profile
            return serializer.save(manager=manager, employer=manager.employer, city=primary_city)
        elif hasattr(user, 'employer_profile'):
            employer = user.employer_profile
            return serializer.save(employer=employer, city=primary_city)
        else:
            logger.warning("Пользователь %s не является работодателем или руководителем", user)
            raise ValidationError("Невозможно создать заказ: пользователь не является работодателем или менеджером.")

    @staticmethod
    def get_tomorrow_orders(user):
        """
        Получение заказов на завтра.
        """
        logger.debug("Получение завтрашних заказов для пользователя: %s", user)
        today = datetime.today().date()
        one_day = timedelta(days=1)
        tomorrow = today + one_day
        primary_city = OrderService.get_primary_city(user)

        if not primary_city:
            return B2COrder.objects.none()

            # Определяем работодателя в зависимости от роли пользователя
        if user.role == 'employer':
            employer = user.employer_profile
        elif user.role == 'manager':
            employer = user.manager_profile.employer  # Для менеджера получаем работодателя
        else:
            return B2COrder.objects.none()  # Возвращаем пустой QuerySet для других ролей

        # Фильтруем заказы по дате и основному городу
        orders = B2COrder.objects.filter(
            Q(order_date=tomorrow) &
            Q(city=primary_city) &
            Q(status=AssignableOrderStatus.IN_PROCESSING) &
            Q(employer=employer)
        )

        order_time = orders.order_by('order_time')

        return order_time

    @staticmethod
    def get_orders_without_dates(user):
        """
        Получение заказов без даты.
        """
        logger.debug("Получение заказов без дат для пользователя: %s", user)
        primary_city = OrderService.get_primary_city(user)  # Получаем основной город пользователя

        if not primary_city:
            return B2COrder.objects.none()  # Возвращаем пустой QuerySet, если нет основного города

            # Определяем работодателя в зависимости от роли пользователя
        if user.role == 'employer':
            employer = user.employer_profile
        elif user.role == 'manager':
            employer = user.manager_profile.employer  # Для менеджера получаем работодателя
        else:
            return B2COrder.objects.none()  # Возвращаем пустой QuerySet для других ролей

        # Фильтруем заказы без даты и по основному городу
        orders = B2COrder.objects.filter(
            Q(order_date__isnull=True) &
            Q(city=primary_city) &
            Q(status=AssignableOrderStatus.IN_PROCESSING) &
            Q(employer=employer)
        )

        order_time = orders.order_by('order_time')

        return order_time

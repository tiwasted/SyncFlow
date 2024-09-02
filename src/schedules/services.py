import logging
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date

from b2c_client_orders.models import B2COrder
from employers.models import Employer
from employees.models import Employee

from orders.services import OrderService

logger = logging.getLogger(__name__)
CustomUser = get_user_model()

class OrderScheduleService:
    """Бизнес-логика для работы с заказами в расписании."""

    @staticmethod
    def get_orders_for_date_and_user(date: int, user_id: int):
        """
        Получение заказов на определенную дату для пользователя.
        """
        try:
            # Получение даты
            date = parse_date(date)
            if not date:
                raise ValidationError("Некорректная дата")

            # Получение пользователя и работодателя по ID
            user = CustomUser.objects.get(id=user_id)
            profile = OrderService.get_user_profile(user)

            # Получение основного города пользователя
            primary_city = OrderService.get_primary_city(user)
            if not primary_city:
                raise ValidationError("Не удалось получить город пользователя")

            # Фильтрация заказов по дате, статусу, работодателю и основному городу
            b2c_orders = B2COrder.objects.filter(
                order_date=date,
                status='in_waiting',
                employer=profile.id,
                city=primary_city
            )

            return b2c_orders
        except CustomUser.DoesNotExist:
            raise ValidationError("Пользователь не найден")
        except Employer.DoesNotExist:
            raise ValidationError("Employer не найден для данного пользователя")
        except ValueError as e:
            logger.error(f"Ошибка при получении заказов: {str(e)}")
            raise ValidationError(f"Произошла ошибка: {str(e)}")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {str(e)}")
            raise ValidationError("Произошла неожиданная ошибка")

    @staticmethod
    def get_employees_by_orders(date=None, user=None):
        """
        Получение списка сотрудников на основании заказов за выбранную дату.
        """

        # Получаем основной город пользователя
        primary_city = OrderService.get_primary_city(user)

        # Получаем заказы на указанную дату
        orders = OrderService.get_orders_by_date_and_time(date)

        # Если основной город указан, фильтруем заказы по этому городу
        if primary_city:
            orders = orders.filter(city=primary_city)

        # Извлекаем уникальных сотрудников из заказов
        employers = Employer.objects.filter(
            assignableorder__in=orders
        ).distinct()

        employees = Employee.objects.filter(
            employer__in=employers
        ).distinct()

        return employees

    @staticmethod
    def get_orders_for_employee(employee=None, date=None):
        """
        Получаем заказы для конкретного сотрудника за выбранную дату.
        """
        if not date:
            raise ValidationError("Дата является обязательной")

        # Получаем основной город через профиль пользователя
        primary_city = OrderService.get_primary_city(employee.user)

        if not primary_city:
            raise ValidationError("Основной город не найден")

        # Фильтруем заказы по дате, основному городу и сотруднику
        orders = B2COrder.objects.filter(
            assigned_employees=employee,
            order_date=date,
            city=primary_city
        )
        return orders

import logging
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date

from b2c_client_orders.models import B2COrder
from employers.models import Employer
from employees.models import Employee
from orders.models import AssignableOrderStatus

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
        logger.info("Начало выполнения функции get_orders_for_date_and_user")
        try:
            # Получение даты
            logger.debug(f"Полученное значение даты: {date}")
            date = parse_date(date)
            if not date:
                logger.error(f"Ошибка: некорректная дата - {date}")
                raise ValidationError("Некорректная дата")

            logger.info(f"Дата после парсинга: {date}")

            # Получение пользователя и работодателя по ID
            logger.debug(f"Полученный user_id: {user_id}")
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                logger.error(f"Пользователь не найден: {user_id}")
                raise ValidationError("Пользователь не найден")

            logger.info(f"Пользователь: {user}")

            # Получение профиля пользователя
            profile = OrderService.get_user_profile(user)
            if profile is None:
                logger.error(f"Не удалось получить профиль для пользователя с ID {user_id}")
                raise ValidationError("Не удалось получить профиль пользователя")

            logger.info(f"Профиль пользователя: {profile}")

            # Получение основного города пользователя
            primary_city = OrderService.get_primary_city(user)
            if primary_city is None:
                logger.error(f"Не удалось получить основной город для пользователя с ID {user_id}")
                raise ValidationError("Не удалось получить город пользователя")

            logger.info(f"Основной город пользователя: {primary_city}")

            if not primary_city:
                raise ValidationError("Не удалось получить город пользователя")

            # Фильтрация заказов по дате, статусу, работодателю и основному городу
            logger.debug(f"Фильтрация заказов на дату {date}, город {primary_city}, статус 'IN_WAITING'")
            orders = OrderService.get_orders_by_date_and_time(
                date=date,
                city=primary_city,
                status=AssignableOrderStatus.IN_WAITING,
                user=user
            )
            logger.info(f"Количество найденных заказов: {len(orders)}")

            if user.role == CustomUser.EMPLOYER:
                logger.debug(f"Фильтрация заказов для работодателя {profile}")
                orders = orders.filter(employer=profile)
                logger.info("Фильтрация заказов по работодателю")
            elif user.role == CustomUser.MANAGER:
                logger.debug(f"Фильтрация заказов для менеджера, работодатель {profile.employer}")
                employer = profile.employer
                orders = orders.filter(employer=employer)
                logger.info("Фильтрация заказов по менеджеру")
            else:
                logger.error(f"Некорректная роль пользователя: {user.role}")
                raise ValidationError("Пользователь не является работодателем или менеджером")

            logger.info("Успешное завершение get_orders_for_date_and_user")
            return orders

        except CustomUser.DoesNotExist:
            logger.error(f"Пользователь с ID {user_id} не существует")
            raise ValidationError("Пользователь не найден")
        except Employer.DoesNotExist:
            logger.error(f"Employer не найден для пользователя с ID {user_id}")
            raise ValidationError("Employer не найден для данного пользователя")
        except ValueError as e:
            logger.error(f"Ошибка при получении заказов: {str(e)}")
            raise ValidationError(f"Произошла ошибка: {str(e)}")
        except Exception as e:
            logger.critical(f"Непредвиденная ошибка: {str(e)}", exc_info=True)
            raise ValidationError("Произошла неожиданная ошибка")

    @staticmethod
    def get_employees_by_orders(date=None, user=None):
        """
        Получение списка сотрудников на основании заказов за выбранную дату.
        """
        logger.info("Начало выполнения функции get_employees_by_orders")

        # Получаем основной город пользователя
        primary_city = OrderService.get_primary_city(user)
        logger.info(f"Основной город пользователя: {primary_city}")

        # Получаем заказы на указанную дату
        orders = OrderService.get_orders_by_date_and_time(date)
        logger.info(f"Заказы на дату {date}: {orders}")

        # Если основной город указан, фильтруем заказы по этому городу
        if primary_city:
            orders = orders.filter(city=primary_city)
            logger.info("Фильтрация заказов по основному городу")

        # Извлекаем уникальных сотрудников из заказов
        employers = Employer.objects.filter(
            assignableorder__in=orders
        ).distinct()
        logger.info(f"Работодатели: {employers}")

        employees = Employee.objects.filter(
            employer__in=employers
        ).distinct()
        logger.info(f"Сотрудники: {employees}")

        logger.info("Успешное завершение функции get_employees_by_orders")
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
            city=primary_city,
            status = AssignableOrderStatus.IN_WAITING
        )

        logger.info(f"Количество заказов для сотрудника: {orders.count()}")
        # Или, если нужно идентификаторы заказов:
        logger.info(f"Заказы для сотрудника: {[order.id for order in orders]}")

        order_time = orders.order_by('order_time')
        logger.info(f"Заказы отсортированы по времени: {order_time}")

        logger.info("Успешное завершение функции get_orders_for_employee")

        return order_time

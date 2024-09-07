from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from django.db.models import Q
import logging

from b2c_client_orders.models import B2COrder
from employees.models import Employee
from employers.models import Employer, EmployerCityAssignment, Manager, ManagerCityAssignment
from orders.models import AssignableOrderStatus
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
    def assign_employees(order, employee_ids):
        """
        Назначение сотрудников на заказ.
        """
        logger.debug("Назначение сотрудников: %s, на заказ: %s", employee_ids, order)

        employees = list(Employee.objects.filter(id__in=employee_ids))
        if len (employees) != len(employee_ids):
            missing_ids = set(employee_ids) - set(e.id for e in employees)
            raise ValidationError(f"Сотрудники с ID {', '.join(map(str, missing_ids))} не найдены")

        order.assign_employees(employees)
        logger.info("Сотрудники: %s, назначены на заказ: %s", employees, order)
        return employees

    @staticmethod
    def get_orders_by_date_and_time(date=None, city=None, status=None):
        """
        Получение заказов по выбранной дате, отсортированных по времени.
        """
        logger.debug("Получение заказов по дате: %s, городу: %s, статусу: %s", date, city, status)
        queryset = B2COrder.objects.all()

        if date:
            queryset = queryset.filter(order_date=date)

        if city:
            queryset = queryset.filter(city=city)

        if status:
            queryset = queryset.filter(status=status)

        queryset = queryset.order_by('order_time')
        logger.info("Получено заказов: %s", queryset)

        return queryset


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
    def update_order(user, serializer):
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
    def update_order_status(order, employee, action, report=''):
        logger.debug("Обновление статуса заказа для заказа: %s, сотрудник: %s, действие: %s", order, employee, action)

        if not order.assigned_employees.filter(id=employee.id).exists():
            logger.warning("Сотрудник не назначен на заказ: %s, заказ: %s", employee, order)
            raise ValidationError("Сотрудник не назначен на заказ")

        # Обновляем статус заказа в зависимости от действия
        if action == 'complete':
            order.status = AssignableOrderStatus.COMPLETED
        elif action == 'cancel':
            order.status = AssignableOrderStatus.CANCELLED
        else:
            raise ValidationError(f"Недопустимое действие: {action}")

        logger.debug(f"Новый статуса {order.status} для заказа {order.id}")

        # Сохраняем отчет, если он был предоставлен
        if report:
            order.report = report

        order.save()

        logger.info("Статус заказа обновлен для заказа: %s, новый статус: %s", order.id, order.status)
        return order

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

        # Фильтруем заказы по дате и основному городу
        return B2COrder.objects.filter(
            Q(order_date=tomorrow) & Q(city=primary_city) & Q(status=AssignableOrderStatus.IN_PROCESSING)
        )

    @staticmethod
    def get_orders_without_dates(user):
        """
        Получение заказов без даты.
        """
        logger.debug("Получение заказов без дат для пользователя: %s", user)
        primary_city = OrderService.get_primary_city(user)  # Получаем основной город пользователя

        if not primary_city:
            return B2COrder.objects.none()  # Возвращаем пустой QuerySet, если нет основного города

        # Фильтруем заказы без даты и по основному городу
        return B2COrder.objects.filter(
            Q(order_date__isnull=True) & Q(city=primary_city) & Q(status=AssignableOrderStatus.IN_PROCESSING)
        )

from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from django.db.models import Q

from b2c_client_orders.models import B2COrder
from employees.models import Employee
from employers.models import Employer, EmployerCityAssignment, Manager, ManagerCityAssignment
from orders.models import AssignableOrderStatus


class OrderService:
    """Бизнес-логика для работы с заказами."""

    @staticmethod
    def get_user_profile(user):
        """
        Возвращает профиль пользователя, если у него есть роль employer или manager.
        """
        if hasattr(user, 'employer_profile'):
            return user.employer_profile
        elif hasattr(user, 'manager_profile'):
            return user.manager_profile
        elif hasattr(user, 'employee_profile'):
            return user.employee_profile
        else:
            raise ValidationError(
                f"Профиль пользователя (ID: {user.id}) не является работодателем, менеджером или сотрудником")

    @staticmethod
    def get_primary_city(user):
        """
        Получение основного города пользователя.
        """
        profile = OrderService.get_user_profile(user)

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
                raise ValidationError("Сотрудник не связан с работодателем")
            primary_city_assignment = EmployerCityAssignment.objects.filter(
                employer=employer,
                is_primary=True
            ).first()
        else:
            raise ValidationError("Профиль пользователя не является работодателем, менеджером или сотрудником")

        if not primary_city_assignment:
            raise ValidationError(f"Основной город не найден для профиля {profile}")

        return primary_city_assignment.city if primary_city_assignment else None

    @staticmethod
    def assign_employees(order, employee_ids):
        """
        Назначение сотрудников на заказ.
        """
        employees = list(Employee.objects.filter(id__in=employee_ids))
        if len (employees) != len(employee_ids):
            missing_ids = set(employee_ids) - set(e.id for e in employees)
            raise ValidationError(f"Сотрудники с ID {', '.join(map(str, missing_ids))} не найдены")
        order.assign_employees(employees)
        return employees

    @staticmethod
    def get_orders_by_date_and_time(date=None, city=None, status=None):
        """
        Получение заказов по выбранной дате, отсортированных по времени.
        """

        queryset = B2COrder.objects.all()

        if date:
            queryset = queryset.filter(order_date=date)

        if city:
            queryset = queryset.filter(city=city)

        if status:
            queryset = queryset.filter(status=status)

        queryset = queryset.order_by('order_time')

        return queryset


class OrderDashboardService:
    """Бизнес-логика для работы с заказами во вкладке Dashboard."""

    @staticmethod
    def create_order(user, serializer):
        """
        Создание заказа.
        """
        primary_city = OrderService.get_primary_city(user)

        if hasattr(user, 'manager_profile'):
            manager = user.manager_profile
            return serializer.save(manager=manager, employer=manager.employer, city=primary_city)
        elif hasattr(user, 'employer_profile'):
            employer = user.employer_profile
            return serializer.save(employer=employer, city=primary_city)
        else:
            raise ValidationError("Невозможно создать заказ: пользователь не является работодателем или менеджером.")

    @staticmethod
    def update_order(user, serializer):
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
        if order.assigned_employee != employee:
            raise ValidationError("Сотрудник не назначен на заказ")

        if action == 'complete':
            order.complete_order()
        elif action == 'cancel':
            order.cancel_order()

        if report:
            order.report = report
            order.save()

        return order

    @staticmethod
    def get_tomorrow_orders(user):
        """
        Получение заказов на завтра.
        """
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
        primary_city = OrderService.get_primary_city(user)  # Получаем основной город пользователя

        if not primary_city:
            return B2COrder.objects.none()  # Возвращаем пустой QuerySet, если нет основного города

        # Фильтруем заказы без даты и по основному городу
        return B2COrder.objects.filter(
            Q(order_date__isnull=True) & Q(city=primary_city) & Q(status=AssignableOrderStatus.IN_PROCESSING)
        )

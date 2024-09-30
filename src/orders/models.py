from django.db import models
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, null=False, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        unique_together = ['name', 'country'] # Чтобы избежать дублирования городов с одинаковыми именами в разных странах

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AssignableOrderStatus(models.TextChoices):
    IN_PROCESSING = 'in_processing', 'В обработке'
    IN_WAITING = 'in_waiting', 'В ожидании'
    COMPLETED = 'completed', 'Выполнен'
    CANCELLED = 'cancelled', 'Отменен'


class AssignableOrder(models.Model):
    status = models.CharField(max_length=20, choices=AssignableOrderStatus.choices, default=AssignableOrderStatus.IN_PROCESSING)
    assigned_employees = models.ManyToManyField('employees.Employee', related_name='%(class)s_assigned_orders')
    report = models.TextField(blank=True, null=True)
    city = models.ForeignKey('orders.City', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_orders')
    payment_method = models.ForeignKey('orders.PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_id = models.CharField(max_length=255, unique=True, null=True,
                                   blank=True)  # Для хранения уникального ID из внешнего API

    class Meta:
        abstract = True

    @property
    def assigned_to_info(self):
        employees = self.assigned_employees.all()
        if len (employees) == 1:
            employee = employees[0]
            return {
                "name": f"{employee.first_name} {employee.last_name}",
                "phone": employee.user.phone
            }
        else:
            # Отображение всех сотрудников
            return [
                {
                    "name": f"{employee.first_name} {employee.last_name}",
                    "phone": employee.user.phone,
                }
                for employee in employees
            ]

    def assign_employees(self, employees):
        if not employees:
            raise ValueError("Список сотрудников не может быть пустым")

        # Назначение сотрудников на заказ
        self.assigned_employees.set(employees)
        self.status = AssignableOrderStatus.IN_WAITING
        self.save()

    def create_schedule_entry(self, employee):
        raise NotImplementedError("Подклассы должны реализовывать create_schedule_entry()")

    def complete_order(self):
        self.status = AssignableOrderStatus.COMPLETED
        logger.debug("Сохранение статуса COMPLETED для заказа %s", self.id)
        self.save()

    def cancel_order(self):
        self.status = AssignableOrderStatus.CANCELLED
        logger.debug("Сохранение статуса CANCELLED для заказа %s", self.id)
        self.save()

    def save(self, *args, **kwargs):
        """Переопределяем метод save, чтобы обновить поле updated_at при любом изменении."""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

from django.db import models
from users.models import CustomUser
from employers.models import Employer
from employees.models import Employee


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В обработке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    )

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='orders')

    order_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in processing')

    order_date = models.DateField()
    order_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    assigned_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders')

    address = models.CharField(max_length=255)
    phone_number_client = models.CharField(max_length=11)
    first_name_client = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order_name

    def assign_employee(self, employee):
        self.assigned_employee = employee
        self.status = 'pending'
        self.save()

    def complete_order(self):
        self.status = 'completed'
        self.save()

    def cancel_order(self):
        self.status = 'cancelled'
        self.save()

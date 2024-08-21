from django.db import models


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


class AssignableOrder(models.Model):
    STATUS_CHOICES = (
        ('in processing', 'В обработке'),
        ('in waiting', 'В ожидании'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in processing')
    assigned_employee = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_assigned_orders')
    employee_name = models.CharField(max_length=100, blank=True, null=True)
    employee_phone = models.CharField(max_length=11, blank=True, null=True)
    report = models.TextField(blank=True, null=True)
    city = models.ForeignKey('orders.City', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_orders')


    class Meta:
        abstract = True


    def save(self, *args, **kwargs):
        if self.assigned_employee:
            self.employee_name = f"{self.assigned_employee.first_name} {self.assigned_employee.last_name}"
            self.employee_phone = self.assigned_employee.user.phone
        else:
            self.employee_name = None
            self.employee_phone = None
        super().save(*args, **kwargs)

    def assign_employee(self, employee):
        self.assigned_employee = employee
        self.status = 'in waiting'
        self.save()

    def complete_order(self):
        self.status = 'completed'
        self.save()

    def cancel_order(self):
        self.status = 'cancelled'
        self.save()

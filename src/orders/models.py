from django.db import models


class AssignableOrder(models.Model):
    STATUS_CHOICES = (
        ('in waiting', 'В ожидании'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in processing')
    assigned_employee = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_assigned_orders')

    class Meta:
        abstract = True

    def __str__(self):
        return self.order_name

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

from django.db import models
from employees.models import Employee


class Schedule(models.Model):
    b2b_order = models.ForeignKey('b2b_client_orders.B2BOrder', on_delete=models.CASCADE, null=True, blank=True, related_name='schedules')
    b2c_order = models.ForeignKey('b2c_client_orders.B2COrder', on_delete=models.CASCADE, null=True, blank=True, related_name='schedules')
    assigned_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='schedules')

    def __str__(self):
        order = self.b2b_order or self.b2c_order
        return f"Schedule for {order} assigned to {self.employee}"

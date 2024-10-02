from django.db import models
from orders.models import AssignableOrder
from employers.models import Employer, Manager
from schedules.models import Schedule


class B2COrder(AssignableOrder):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='b2c_orders')
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, related_name='b2c_orders')

    order_name = models.CharField(max_length=255, null=True)
    order_date = models.DateField(null=True)
    order_time = models.TimeField(null=True)
    address = models.CharField(max_length=255, null=True)
    phone_number_client = models.CharField(max_length=255, null=True)
    name_client = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    description = models.TextField(null=True)

    def create_schedule_entries(self, employees):
        for employee in employees:
            Schedule.objects.create(
                b2c_order=self,
                assigned_employee=employee,
            )


class B2COrderImage(models.Model):
    order = models.ForeignKey(B2COrder, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='order_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for order {self.order.id}"

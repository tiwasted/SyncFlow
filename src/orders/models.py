from django.db import models
from users.models import CustomUser
from employers.models import Employer
from employees.models import Employee


class Order(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    )

    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='orders')

    order_name = models.CharField(max_length=255)

    order_date = models.DateField()
    order_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    address = models.CharField(max_length=255)
    phone_number_client = models.CharField(max_length=11)
    first_name_client = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.order_name

from django.db import models
from orders.models import AssignableOrder
from employers.models import Employer


class B2COrder(AssignableOrder):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='b2c_orders')

    order_name = models.CharField(max_length=255)
    order_date = models.DateField()
    order_time = models.TimeField()
    address = models.CharField(max_length=255)
    phone_number_client = models.CharField(max_length=11)
    name_client = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_time.strftime('%H:%M') + ' ' + self.order_name

    @property
    def formatted_order_time(self):
        return self.order_time.strftime('%H:%M')


class B2COrderImage(models.Model):
    order = models.ForeignKey(B2COrder, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='order_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for order {self.order.id}"

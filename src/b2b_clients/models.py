from django.db import models


class B2BClient(models.Model):
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    order_date = models.DateTimeField()
    order_time = models.TimeField()
    notes = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

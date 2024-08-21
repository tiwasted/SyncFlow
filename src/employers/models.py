from django.db import models

from orders.models import Country, City
from users.models import CustomUser


class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=50)
    company_description = models.TextField()
    countries = models.ManyToManyField(Country, related_name='employers', blank=True)
    cities = models.ManyToManyField(City, related_name='employers', blank=True)

    def __str__(self):
        return self.company_name
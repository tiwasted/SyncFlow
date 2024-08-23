from django.db import models

from orders.models import Country, City
from users.models import CustomUser


class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=50)
    company_description = models.TextField()
    countries = models.ManyToManyField(Country, related_name='employers', blank=True)
    cities = models.ManyToManyField(City, related_name='employers', blank=True)


class EmployerCity(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='employer_city_relations')
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('employer', 'city')

    def __str__(self):
        return f"{self.employer.company_name} - {self.city.name}"

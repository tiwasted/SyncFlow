from django.db import models

from orders.models import Country, City, PaymentMethod
from users.models import CustomUser


class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    company_name = models.CharField(max_length=50)
    company_description = models.TextField()
    selected_countries = models.ManyToManyField(Country, related_name='employers', blank=True)
    selected_cities = models.ManyToManyField(City, related_name='employers', blank=True)
    available_payment_methods = models.ManyToManyField(PaymentMethod, related_name='employers', blank=True)


    def __str__(self):
         return f"Employer: {self.company_name}"


class EmployerCityAssignment(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='city_assignments')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employer', 'city')

    def __str__(self):
        return f"{self.employer.user.phone} - {self.city.name} (Primary: {self.is_primary})"


class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='manager_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='managers')
    is_active = models.BooleanField(default=True)
    cities = models.ManyToManyField(City, related_name='managers')

    def __str__(self):
        return f"Manager: {self.first_name}"


class ManagerCityAssignment(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='city_assignments')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('manager', 'city')

    def __str__(self):
        return f"{self.manager.user.phone} - {self.city.name}"

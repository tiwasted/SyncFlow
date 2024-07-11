from django.db import models
from users.models import CustomUser


class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=50)
    company_description = models.TextField()

    def __str__(self):
        return self.company_name
from django.db import models
from users.models import CustomUser
from employers.models import Employer


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='employees')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def delete(self, *args, **kwargs):
        # Деактивируем сотрудника, но не удаляем из базы
        self.is_active = False
        self.save()

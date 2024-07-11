from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    EMPLOYER = 'employer'
    EMPLOYEE = 'employee'
    ROLE_CHOICES = [
        (EMPLOYER, 'Employer'),
        (EMPLOYEE, 'Employee'),
    ]

    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

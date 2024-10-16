from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone=None, password=None, **extra_fields):
        if not phone:
            raise ValueError('Пользователи должны иметь номер телефона.')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('У суперпользователя должно быть значение is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('У суперпользователя должно быть значение is_superuser=True.')

        if not phone:
            raise ValueError('У суперпользователей должен быть адрес электронной почты.')

        return self.create_user(phone, password=password, **extra_fields)

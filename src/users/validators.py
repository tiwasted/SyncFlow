from django.core.exceptions import ValidationError
import re


def validate_password(value):
    if not re.findall(r'[A-Z]', value):
        raise ValidationError("Пароль должен содержать хотя одну заглавную букву.")
    if not re.findall(r'\d', value):
        raise ValidationError("Пароль должен содержаться хотя бы одну цифру.")

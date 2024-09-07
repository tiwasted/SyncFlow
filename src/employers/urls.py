from django.urls import path
from .views.registration_employer_views import EmployerRegistrationView
from .views.password_change import ChangePasswordView


urlpatterns = [
    path('register/', EmployerRegistrationView.as_view(), name='employer_registration'),  # Регистрация Работодателя (POST)
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

from django.urls import path
from .views.registration_employer_views import EmployerRegistrationView


urlpatterns = [
    path('register/', EmployerRegistrationView.as_view(), name='employer_registration'),  # Регистрация Работодателя (POST)
]

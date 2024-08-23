from django.urls import path
from .views.registration_employer_views import EmployerRegistrationView
from .views.password_change_views import ChangePasswordView
from .views.employer_views import EmployerView
from .views.employer_city_views import EmployerCitiesView, EmployerCityManagementView


urlpatterns = [
    path('register/', EmployerRegistrationView.as_view(), name='employer_registration'),  # Регистрация Работодателя (POST)
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('employer-preferences/', EmployerView.as_view(), name='employer-preferences'),

    path('employer-cities/', EmployerCitiesView.as_view(), name='employer-city'),
    path('manage-city/', EmployerCityManagementView.as_view(), name='employer-manage-city'),
]

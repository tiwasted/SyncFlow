from django.urls import path
from .views.registration_employer_views import EmployerRegistrationView
from .views.password_change_views import ChangePasswordView
from .views.employer_views import EmployerView
from .views.employer_city_views import AddCountriesView, AddCitiesView, AddedCountriesWithCitiesView


urlpatterns = [
    path('register/', EmployerRegistrationView.as_view(), name='employer_registration'),  # Регистрация Работодателя (POST)
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('employer-preferences/', EmployerView.as_view(), name='employer-preferences'),

    path('add-countries/', AddCountriesView.as_view(), name='add-countries'),
    path('add-cities/', AddCitiesView.as_view(), name='add-cities'),

    path('added-countries-with-cities/', AddedCountriesWithCitiesView.as_view(), name='added-countries-with-cities'),
]

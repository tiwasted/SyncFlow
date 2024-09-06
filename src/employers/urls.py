from django.urls import path
from .views.registration_employer_views import EmployerRegistrationView
from .views.employer_views import EmployerView
from .views.role_views import RoleListView, RoleCreateView
from .views.employer_city_views import AddCountriesView, AddCitiesView, AvailableCitiesView, ListCitiesView
from .views.manager_views import ManagerListView, ManagerDetailView, ManagerUpdateView, ManagerDeleteView
from .views.assign_city_to_manager import AssignCityToManagerView, ManagerCitiesView
from .views.set_city_views import SetPrimaryCityView, GetPrimaryCityView


urlpatterns = [
    path('register/', EmployerRegistrationView.as_view(), name='employer_registration'),  # Регистрация Работодателя (POST)
    path('employer-preferences/', EmployerView.as_view(), name='employer-preferences'),

    path('add-countries/', AddCountriesView.as_view(), name='add-countries'),
    path('add-cities/', AddCitiesView.as_view(), name='add-cities'),

    path('roles/', RoleListView.as_view(), name='roles-list'),
    path('available-cities/', AvailableCitiesView.as_view(), name='available-cities'),
    path('create-role/', RoleCreateView.as_view(), name='create-role'),

    path('managers/', ManagerListView.as_view(), name='manager-list'),
    path('managers/<int:pk>/', ManagerDetailView.as_view(), name='manager-detail'),
    path('manager/edit/<int:pk>/', ManagerUpdateView.as_view(), name='manager-edit'),
    path('manager/<int:pk>/delete/', ManagerDeleteView.as_view(), name='manager-delete'),

    path('manager/assign-city/<int:manager_id>/', AssignCityToManagerView.as_view(), name='assign-city-to-manager'),
    path('manager/<int:manager_id>/cities/', ManagerCitiesView.as_view(), name='manager-cities'),

    path('dashboard/list-cities/', ListCitiesView.as_view(), name='list-cities'),
    path('select-primary-city/', SetPrimaryCityView.as_view(), name='select-primary-city'),
    path('get-primary-city/', GetPrimaryCityView.as_view(), name='get-primary-city'),
]

from django.urls import path
from .views.create_employee_views import EmployeeCreateView


urlpatterns = [
    path('create-employee/', EmployeeCreateView.as_view(), name='employee_create'),
]

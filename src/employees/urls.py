from django.urls import path
from .views.employee_create_views import EmployeeCreateView


urlpatterns = [
    path('create-employee/', EmployeeCreateView.as_view(), name='employee_create'),
]

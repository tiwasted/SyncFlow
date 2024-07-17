from django.urls import path
from .views.employee_views import EmployeeListView
from .views.create_employee_views import EmployeeCreateView


urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='employee-list'),

    path('create-employee/', EmployeeCreateView.as_view(), name='employee_create'),
]

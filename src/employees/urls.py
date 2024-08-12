from django.urls import path
from .views.employee_views import EmployeeListView, EmployeeDeleteView
from .views.create_employee_views import EmployeeCreateView
from .views.assigned_order_views import AssignedOrderEmployeeListView
from .views.edit_employee_views import EmployeeUpdateView


urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('edit/<int:pk>', EmployeeUpdateView.as_view(), name='employee-edit'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

    path('assigned-orders/', AssignedOrderEmployeeListView.as_view(), name='assigned-orders-list'),

]

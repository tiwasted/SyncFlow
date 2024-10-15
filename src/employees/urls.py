from django.urls import path

from employers.views.employer_payment_method_views import AvailablePaymentMethodsView
from .views.employee_views import EmployeeListView, EmployeeDeleteView, AssigningEmployeeToOrderListView
from .views.assigned_order_views import AssignedOrderEmployeeListView
from .views.edit_employee_views import EmployeeUpdateView
from b2c_client_orders.views.load_image_views import AddOrderImageView, DeleteOrderImageView


urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('edit/<int:pk>/', EmployeeUpdateView.as_view(), name='employee-edit'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

    path('assigned-orders/', AssignedOrderEmployeeListView.as_view(), name='assigned-orders-list'),

    path('assigning-list/', AssigningEmployeeToOrderListView.as_view(), name='assigning-employee-list'),

    path('orders/<int:order_id>/add-image/', AddOrderImageView.as_view(), name='add-order-image'),
    path('orders/images/<int:image_id>/delete/', DeleteOrderImageView.as_view(), name='delete-order-image'),

    path('list-payment-methods/', AvailablePaymentMethodsView.as_view(), name='list-payment-methods'),
]

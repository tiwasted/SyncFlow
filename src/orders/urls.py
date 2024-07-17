from django.urls import path
from .views.create_order_views import OrderCreateView
from .views.order_views import OrderListEmployerView, OrderListEmployeeView
from .views.edit_order_views import OrderEditView
from .views.delete_order_views import OrderDeleteView
from .views.assign_employee_views import AssignEmployeeToOrderView
from .views.status_order_views import OrderStatusUpdateView


urlpatterns = [
    path('employer/orders/', OrderListEmployerView.as_view(), name='orders-list-employer'),
    path('employee/orders/', OrderListEmployeeView.as_view(), name='orders-list-employee'),

    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/edit/', OrderEditView.as_view(), name='order-edit'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),

    path('<int:pk>/assign/', AssignEmployeeToOrderView.as_view(), name='order-assign-employee'),
    path('<int:pk>/update-status/', OrderStatusUpdateView.as_view(), name='order-update-status'),
]

from django.urls import path
from .views.create_order_views import OrderCreateView
from .views.read_order_views import OrderListEmployerView, OrderListEmployeeView
from .views.edit_order_views import OrderEditView
from .views.delete_order_views import OrderDeleteView
from .views.order_assign_views import OrderAssignEmployeeView
from .views.status_order_views import OrderStatusUpdateView


urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/edit/', OrderEditView.as_view(), name='order-edit'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),

    path('employer/order/', OrderListEmployerView.as_view(), name='order-list-employer'),
    path('employee/order/', OrderListEmployeeView.as_view(), name='order-list-employee'),
    path('employee/<int:pk>/update-status/', OrderStatusUpdateView.as_view(), name='order-update-status'),

    path('assign/<int:pk>/', OrderAssignEmployeeView.as_view(), name='order-assign-employee'),
]

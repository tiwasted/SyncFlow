from django.urls import path
from .views.create_order_views import OrderCreateView
from .views.read_order_views import OrderListEmployerView
from .views.edit_order_views import OrderEditView
from .views.order_assign_views import OrderAssignEmployeeView


urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('list/', OrderListEmployerView.as_view(), name='order-list-employer'),
    path('<int:pk>/edit/', OrderEditView.as_view(), name='order-edit'),


    path('assign/<int:pk>/', OrderAssignEmployeeView.as_view(), name='order-assign-employee'),
]

from django.urls import path
from .views.order_create_views import OrderCreateView


urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
]

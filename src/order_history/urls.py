from django.urls import path
from .views.order_history_views import OrderHistoryView


urlpatterns = [
    path('history/', OrderHistoryView.as_view(), name='order-history'),
]

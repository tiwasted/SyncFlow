from django.urls import path
from b2c_client_orders.views.image_views import B2COrderImageView

urlpatterns = [
    path('orders/<int:order_id>/image/', B2COrderImageView.as_view(), name='order-image'),
]

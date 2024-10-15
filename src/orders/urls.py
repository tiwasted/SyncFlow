from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views.b2b_order_views import B2BOrderViewSet
from orders.views.b2c_order_views import B2COrderViewSet
from orders.views.order_assignment_views import OrderAssignmentViewSet
from orders.views.order_status_views import OrderStatusViewSet
from orders.views.order_city_views import CountryListView, CityListView, CitiesByCountryView
from orders.views.order_payment_method_views import PaymentMethodListView
from integration.views import webhook_handler


router = DefaultRouter()

router.register(r'b2b-orders', B2BOrderViewSet, basename='b2b-order')
router.register(r'b2c-orders', B2COrderViewSet, basename='b2c-order')
router.register(r'order-assignment', OrderAssignmentViewSet, basename='order-assignment')
router.register(r'order-status', OrderStatusViewSet, basename='order-status')


urlpatterns = [
    path('', include(router.urls)),

    path('countries/', CountryListView.as_view(), name='country-list'),
    path('cities/', CityListView.as_view(), name='city-list'),
    path('countries/<int:country_id>/cities/', CitiesByCountryView.as_view(), name='cities-by-country'),

    path('payment-methods/', PaymentMethodListView.as_view(), name='payment-method-list'),

    path('webhook/', webhook_handler, name='webhook_handler'),
]

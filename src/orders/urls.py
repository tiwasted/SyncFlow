from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views.b2b_order_views import B2BOrderViewSet
from orders.views.b2c_order_views import B2COrderViewSet
from orders.views.city_order_views import CountryListView, CityListView, CitiesByCountryView


router = DefaultRouter()
router.register(r'b2b-orders', B2BOrderViewSet, basename='b2b-order')
router.register(r'b2c-orders', B2COrderViewSet, basename='b2c-order')


urlpatterns = [
    path('', include(router.urls)),

    path('countries/', CountryListView.as_view(), name='country-list'),
    path('cities/', CityListView.as_view(), name='city-list'),
    path('countries/<int:country_id>/cities/', CitiesByCountryView.as_view(), name='cities-by-country'),
]

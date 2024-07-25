from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views.b2b_order_views import B2BOrderViewSet
from orders.views.b2c_order_views import B2COrderViewSet
from orders.views.schedule_order_views import OrderScheduleViewSet


router = DefaultRouter()
router.register(r'b2b-orders', B2BOrderViewSet, basename='b2b-order')
router.register(r'b2c-orders', B2COrderViewSet, basename='b2c-order')
router.register(r'schedule', OrderScheduleViewSet, basename='schedule')


urlpatterns = [
    path('', include(router.urls)),

]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.order_history_views import B2BOrderHistoryViewSet, B2COrderHistoryViewSet


router = DefaultRouter()
router.register(r'b2b-history', B2BOrderHistoryViewSet, basename='b2border-history')
router.register(r'b2c-history', B2COrderHistoryViewSet, basename='b2corder-history')


urlpatterns = [
    path('', include(router.urls)),
]

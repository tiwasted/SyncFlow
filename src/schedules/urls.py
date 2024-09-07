from django.urls import path, include
from rest_framework.routers import DefaultRouter
from schedules.views.schedule_order_views import OrderScheduleViewSet


router = DefaultRouter()
router.register(r'schedule', OrderScheduleViewSet, basename='schedule')


urlpatterns = [
    path('', include(router.urls)),


]

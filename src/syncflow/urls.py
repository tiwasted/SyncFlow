from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('employers/', include('employers.urls')),
    path('employees/', include('employees.urls')),
    path('b2c/', include('b2c_client_orders.urls')),
    path('b2b/', include('b2b_client_orders.urls')),
    path('orders/', include('orders.urls')),
    path('schedules/', include('schedules.urls')),
    path('order-history/', include('order_history.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

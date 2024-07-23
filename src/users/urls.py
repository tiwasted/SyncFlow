from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserLoginView

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('auth/login/', UserLoginView.as_view(), name='login'),
]
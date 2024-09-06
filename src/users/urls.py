from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views.views import UserLoginView
from users.views.password_change_views import ChangePasswordView

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
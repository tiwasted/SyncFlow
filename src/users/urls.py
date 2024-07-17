from django.urls import path
from .views import UserLoginView

urlpatterns = [
    path('auth/login/', UserLoginView.as_view(), name='login'),
]
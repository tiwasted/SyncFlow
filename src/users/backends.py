from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class AuthBackend(ModelBackend):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Поиск пользователя по телефону
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """Получение экземпляра пользователя по ID."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

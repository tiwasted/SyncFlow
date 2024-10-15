from rest_framework import generics, permissions, status
from rest_framework.response import Response
from users.models import CustomUser
from users.serializers.password_change_serializers import ChangePasswordSerializer


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Проверка старого пароля
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Неверный текущий пароль."]}, status=status.HTTP_400_BAD_REQUEST)

            # Установка нового пароля
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response({"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminPasswordResetView(APIView):
    """
    Представление для сброса пароля пользователя администратором
    """
    permission_classes = [IsAdminUser]  # Доступ только для администраторов

    def post(self, request):
        phone = request.data.get('phone')
        new_password = request.data.get('new_password')

        if not phone or not new_password:
            return Response({"error": "Требуется номер телефона и новый пароль."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({"error": "Пользователь с таким номером телефона не существует."}, status=status.HTTP_404_NOT_FOUND)

        # Устанавливаем новый пароль
        user.set_password(new_password)
        user.save()

        return Response({"message": f"Пароль для пользователя с телефоном {phone} был успешно сброшен."}, status=status.HTTP_200_OK)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from users.models import CustomUser
from employers.models import Manager

from employers.serializers.manager_serializers import ManagerCreateSerializer, ManagerSerializer

User = get_user_model()


# Создание менеджеров через Работодателя
class ManagerCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.role != 'employer':
            return Response({"error": "Только Employer может создавать Employee."},
                            status=status.HTTP_403_FORBIDDEN)

        if not hasattr(request.user, 'employer_profile'):
            return Response({"error": "Этот пользователь не связан с профилем работодателя."},
                            status=status.HTTP_400_BAD_REQUEST)

        employer = request.user.employer_profile
        print("Работодатель из профиля пользователя:", employer)
        serializer = ManagerCreateSerializer(data=request.data, context={'employer': employer})
        if serializer.is_valid():
            user = serializer.save(employer=employer)
            return Response({"message": "Manager создан успешно"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Чтение менеджеров для Работодателя
class ManagerListView(generics.ListAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            employer = user.employer_profile
            return Manager.objects.filter(employer=employer)
        return Manager.objects.none()


# Редактирование менеджеров через Работодателя
class ManagerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.EMPLOYER:
            return Manager.objects.filter(employer=user.employer_profile)
        return Manager.objects.none()


# Удаление менеджеров через Работодателя
class ManagerDeleteView(generics.DestroyAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.delete()

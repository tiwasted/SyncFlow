from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from employers.permissions import IsEmployer
from orders.permissions import IsEmployerOrManager
from users.models import CustomUser
from employers.models import Manager
from orders.services import OrderService

from employers.serializers.manager_serializers import ManagerSerializer, ManagerSerializerUpdate

User = get_user_model()


# Чтение менеджеров для Работодателя
class ManagerListView(generics.ListAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrManager]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        profile = OrderService.get_user_profile(user)

        if hasattr(profile, 'employer_profile'):
            return Manager.objects.filter(employer=profile.employer)

        elif hasattr(profile, 'manager_profile'):
            return Manager.objects.filter(manager=profile.manager)

        return queryset


class ManagerDetailView(generics.RetrieveAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    lookup_field = 'pk'


# Редактирование менеджеров через Работодателя
class ManagerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializerUpdate
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.EMPLOYER:
            return Manager.objects.filter(employer=user.employer_profile)
        return Manager.objects.none()


# Удаление менеджеров через Работодателя
class ManagerDeleteView(generics.DestroyAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.delete()

    def delete(self, request, *args, **kwargs):
        self.objects = self.get_object()
        self.perform_destroy(self.objects)
        return Response({'detail': 'Менеджер успешно удален'}, status=status.HTTP_204_NO_CONTENT)

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from employers.models import Employer
from employees.models import Employee


class CanViewOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить доступ, если пользователь - работодатель этого заказа
        if hasattr(request.user, 'employer_profile'):
            return obj.employer == request.user.employer_profile
        # Разрешить доступ, если пользователь - назначенный сотрудник
        if hasattr(request.user, 'employee_profile'):
            return obj.assigned_employee == request.user.employee_profile
        return False


class BaseOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, CanViewOrder]

    def get_queryset(self):
        user = self.request.user
        try:
            employer = user.employer_profile
            return self.queryset.filter(employer=employer)
        except Employer.DoesNotExist:
            return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def assign_employee(self, request, pk=None):
        order = self.get_object()
        employee_id = request.data.get('employee_id')

        if not employee_id:
            return Response({"error": "Требуется ID сотрудника"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Сотрудник не найден"}, status=status.HTTP_404_NOT_FOUND)

        order.assign_employee(employee)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=['post'])
    def complete_order(self, request, pk=None):
        order = self.get_object()

        try:
            employee = request.user.employee_profile
        except ObjectDoesNotExist:
            return Response({"error": "Вы не являетесь сотрудником"}, status=status.HTTP_403_FORBIDDEN)

        if order.assigned_employee != employee:
            return Response({"error": "Вы не назначены на этот заказ"}, status=status.HTTP_403_FORBIDDEN)

        order.complete_order()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()

        try:
            employee = request.user.employee_profile
        except ObjectDoesNotExist:
            return Response({"error": "Вы не являетесь сотрудником"}, status=status.HTTP_403_FORBIDDEN)

        if order.assigned_employee != employee:
            return Response({"error": "Вы не назначены на этот заказ"}, status=status.HTTP_403_FORBIDDEN)

        order.cancel_order()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

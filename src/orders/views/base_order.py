from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from employers.models import Employer
from employees.models import Employee
from schedules.models import Schedule
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder
from orders.permissions import CanViewOrder


class BaseOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, CanViewOrder]

    def get_queryset(self):
        user = self.request.user
        try:
            employer = user.employer_profile
            return self.queryset.filter(employer=employer, status='in processing')
        except Employer.DoesNotExist:
            return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save()

    # Назначение сотрудника на заказ
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
        # Назначение сотрудника
        order.assign_employee(employee)

        if isinstance(order, B2BOrder):
            Schedule.objects.create(b2b_order=order, assigned_employee=employee)
        elif isinstance(order, B2COrder):
            Schedule.objects.create(b2c_order=order, assigned_employee=employee)

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    # Завершение заказа сотрудником
    @action(detail=True, methods=['post'])
    def complete_order(self, request, pk=None):
        order = self.get_object()

        try:
            employee = request.user.employee_profile
        except ObjectDoesNotExist:
            return Response({"error": "Вы не являетесь сотрудником"}, status=status.HTTP_403_FORBIDDEN)

        if order.assigned_employee != employee:
            return Response({"error": "Вы не назначены на этот заказ"}, status=status.HTTP_403_FORBIDDEN)

        report = request.data.get('report', '')
        order.complete_order()

        if report:
            order.report = report
            order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    # Отмена заказа сотрудником
    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()

        try:
            employee = request.user.employee_profile
        except ObjectDoesNotExist:
            return Response({"error": "Вы не являетесь сотрудником"}, status=status.HTTP_403_FORBIDDEN)

        if order.assigned_employee != employee:
            return Response({"error": "Вы не назначены на этот заказ"}, status=status.HTTP_403_FORBIDDEN)

        report = request.data.get('report', '')
        order.cancel_order()

        if report:
            order.report = report
            order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)

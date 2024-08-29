from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from employees.models import Employee
from schedules.models import Schedule
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder
from orders.permissions import CanViewOrder, RoleBasedPermission


class BaseOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, CanViewOrder, RoleBasedPermission]


    def perform_create(self, serializer):
        user = self.request.user

        if hasattr(user, 'manager_profile'):
            manager = user.manager_profile
            primary_city_assignment = manager.city_assignments.filter(is_primary=True).first()
            primary_city = primary_city_assignment.city if primary_city_assignment else None
            serializer.save(manager=manager, employer=manager.employer, city=primary_city)

        elif hasattr(user, 'employer_profile'):
            employer = user.employer_profile
            primary_city_assignment = employer.city_assignments.filter(is_primary=True).first()
            primary_city = primary_city_assignment.city if primary_city_assignment else None
            serializer.save(employer=employer, city=primary_city)

        else:
            raise ValidationError("Невозможно создать заказ: пользователь не является работодателем или менеджером.")

    def perform_update(self, serializer):
        user = self.request.user

        if hasattr(user, 'manager_profile'):
            manager = user.manager_profile
            serializer.save(manager=manager, employer=manager.employer)
        elif hasattr(user, 'employer_profile'):
            employer = user.employer_profile
            serializer.save(employer=employer)
        else:
            serializer.save()


    # Назначение сотрудников на заказ
    @action(detail=True, methods=['post'])
    def assign_employee(self, request, pk=None):
        order = self.get_object()
        employee_ids = request.data.get('employee_ids')

        # Если пришел один ID, преобразовываем его в список
        if isinstance(employee_ids, int):
            employee_ids = [employee_ids]
        elif not employee_ids or not isinstance(employee_ids, list):
            return Response({"error": "Требуется ID сотрудника или список ID сотрудников"}, status=status.HTTP_400_BAD_REQUEST)

        assigned_employees = []
        for employee_id in employee_ids:
            try:
                employee = Employee.objects.get(id=employee_id)
            except Employee.DoesNotExist:
                return Response({"error": f"Сотрудник с ID {employee_id} не найден"}, status=status.HTTP_404_NOT_FOUND)

        # Назначение сотрудника на заказ
        order.assign_employee(employee)
        assigned_employees.append(employee)

        # Создание записи в расписании
        if isinstance(order, B2BOrder):
            Schedule.objects.create(b2b_order=order, assigned_employee=employee)
        elif isinstance(order, B2COrder):
            Schedule.objects.create(b2c_order=order, assigned_employee=employee)

        serializer = self.get_serializer(order)
        return Response({
            "order": serializer.data,
            "assigned_employees": [employee.id for employee in assigned_employees]
        })

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

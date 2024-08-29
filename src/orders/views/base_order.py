from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
import logging

from employees.models import Employee
from orders.permissions import CanViewOrder, RoleBasedPermission

logger = logging.getLogger(__name__)


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
        employee_ids = request.data.get('employee_ids', [])

        if not employee_ids:
            return Response({"error": "Требуется список ID сотрудников"}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(employee_ids, list):
            employee_ids = [employee_ids]

        try:
            with transaction.atomic():
                employees = list(Employee.objects.filter(id__in=employee_ids))

                if len(employees) != len(employee_ids):
                    missing_ids = set(employee_ids) - set(e.id for e in employees)
                    return Response({"error": f"Сотрудники с ID {', '.join(map(str, missing_ids))} не найдены"},
                                    status=status.HTTP_404_NOT_FOUND)

                order.assign_employees(employees)
                # order.create_schedule_entries(employees)

                serializer = self.get_serializer(order)
                return Response({
                    "order": serializer.data,
                    "assigned_employees": [e.id for e in employees]
                })

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Ошибка при назначении сотрудников на заказ: {order.id} {str(e)}")
            return Response({"error": "Произошла ошибка при назначении сотрудников на заказ"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

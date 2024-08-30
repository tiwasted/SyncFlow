from django.core.exceptions import ValidationError
from employees.models import Employee


class OrderService:
    @staticmethod
    def get_primary_city(user):
        profile = getattr(user, 'manager_profile', None) or getattr(user, 'employer_profile', None)
        if profile:
            primary_city_assignment = profile.city_assignments.filter(is_primary=True).first()
            return primary_city_assignment.city if primary_city_assignment else None
        return None

    @staticmethod
    def create_order(user, serializer):
        primary_city = OrderService.get_primary_city(user)

        if hasattr(user, 'manager_profile'):
            manager = user.manager_profile
            return serializer.save(manager=manager, employer=manager.employer, city=primary_city)
        elif hasattr(user, 'employer_profile'):
            employer = user.employer_profile
            return serializer.save(employer=employer, city=primary_city)
        else:
            raise ValidationError("Невозможно создать заказ: пользователь не является работодателем или менеджером.")

    @staticmethod
    def update_order(user, serializer):
        if hasattr(user, 'manager_profile'):
            manager = user.manager_profile
            return serializer.save(manager=manager, employer=manager.employer)
        elif hasattr(user, 'employer_profile'):
            employer = user.employer_profile
            return serializer.save(employer=employer)
        else:
            return serializer.save()

    @staticmethod
    def assign_employees(order, employee_ids):
        employees = list(Employee.objects.filter(id__in=employee_ids))
        if len (employees) != len(employee_ids):
            missing_ids = set(employee_ids) - set(e.id for e in employees)
            raise ValidationError(f"Сотрудники с ID {', '.join(map(str, missing_ids))} не найдены")
        order.assign_employees(employees)
        return employees

    @staticmethod
    def update_order_status(order, employee, action, report=''):
        if order.assigned_employee != employee:
            raise ValidationError("Сотрудник не назначен на заказ")

        if action == 'complete':
            order.complete_order()
        elif action == 'cancel':
            order.cancel_order()

        if report:
            order.report = report
            order.save()

        return order

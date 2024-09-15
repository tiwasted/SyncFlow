from django.core.exceptions import ValidationError
import logging

from employees.models import Employee

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OrderAssignmentService:
    @staticmethod
    def assign_employees(order, employee_ids):
        """
        Назначение сотрудников на заказ.
        """
        logger.debug("Назначение сотрудников: %s, на заказ: %s", employee_ids, order)

        employees = list(Employee.objects.filter(id__in=employee_ids))
        if len (employees) != len(employee_ids):
            missing_ids = set(employee_ids) - set(e.id for e in employees)
            raise ValidationError(f"Сотрудники с ID {', '.join(map(str, missing_ids))} не найдены")

        order.assign_employees(employees)
        logger.info("Сотрудники: %s, назначены на заказ: %s", employees, order)
        return employees

from django.core.exceptions import ValidationError
import logging

from orders.models import AssignableOrderStatus

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OrderStatusService:
    """Бизнес-логика для работы со статусами заказов."""

    @staticmethod
    def update_order_status(order, employee, action, report=''):
        """
        Логика обновления статуса заказа.
        """
        logger.debug("Обновление статуса заказа для заказа: %s, сотрудник: %s, действие: %s", order, employee, action)

        if not order.assigned_employees.filter(id=employee.id).exists():
            logger.warning("Сотрудник не назначен на заказ: %s, заказ: %s", employee, order)
            raise ValidationError("Сотрудник не назначен на заказ")

        # Обновляем статус заказа в зависимости от действия
        if action == 'complete':
            order.status = AssignableOrderStatus.COMPLETED
        elif action == 'cancel':
            order.status = AssignableOrderStatus.CANCELLED
        else:
            raise ValidationError(f"Недопустимое действие: {action}")

        logger.debug(f"Новый статуса {order.status} для заказа {order.id}")

        # Сохраняем отчет, если он был предоставлен
        if report:
            order.report = report

        order.save()

        logger.info("Статус заказа обновлен для заказа: %s, новый статус: %s", order.id, order.status)
        return order

import logging
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date

from b2c_client_orders.models import B2COrder
from employers.models import Employer

logger = logging.getLogger(__name__)
CustomUser = get_user_model()

class OrderScheduleService:
    @staticmethod
    def get_orders_for_date_and_user(date, user_id):
        try:
            date = parse_date(date)
            if not date:
                raise ValidationError("Некорректная дата")

            user = CustomUser.objects.get(id=user_id)
            employer = user.employer_profile

            b2c_orders = B2COrder.objects.filter(order_date=date, status='in_waiting', employer=employer.id)

            return b2c_orders
        except CustomUser.DoesNotExist:
            raise ValidationError("Пользователь не найден")
        except Employer.DoesNotExist:
            raise ValidationError("Employer не найден для данного пользователя")
        except ValueError as e:
            logger.error(f"Ошибка при получении заказов: {str(e)}")
            raise ValidationError(f"Произошла ошибка: {str(e)}")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {str(e)}")
            raise ValidationError("Произошла неожиданная ошибка")

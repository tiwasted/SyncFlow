import logging
from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from b2c_client_orders.models import B2COrder
from employers.models import Employer
from orders.models import City


logger = logging.getLogger(__name__)


def save_lead_to_db(lead_data):
    """Сохраняет новый или обновленный заказ непосредственно в базе данных."""
    try:
        # Проверьте наличие external_id
        external_id = lead_data.get("external_id")
        if not external_id:
            logger.error(f"Пропущенный заказ без external_id: {lead_data}")
            return

        employer = Employer.objects.get(id=1)  # Dezcity

        date_time = lead_data.get("date")
        if date_time and " " in date_time:
            order_date_str, order_time_str = date_time.split(" ")
            order_date = datetime.strptime(order_date_str, "%Y-%m-%d").date()
            order_time = datetime.strptime(order_time_str, "%H:%M:%S").time()
        else:
            logger.error(f"Неправильный формат даты: {date_time}")
            return

        # Извлекать имя клиента из контактов
        contacts = lead_data.get("contacts", [])
        name_client = contacts[0]["name"] if contacts else ""

        # Используйте данные с уже подобранным городом для сохранения в базе данных
        city_name = lead_data.get("city", {}).get("name")
        country_name = lead_data.get("city", {}).get("country")
        if city_name and country_name:
            try:
                city = City.objects.get(name=city_name, country__name=country_name)
            except City.DoesNotExist:
                logger.error(f"City {city_name} in {country_name} does not exist.")
                return
        else:
            city = None

        # Разбор с updated_at
        updated_at_str = lead_data.get("updated_at")
        updated_at = parse_datetime(updated_at_str) if updated_at_str else timezone.now()

        # Сохранение или обновление заказа
        order, created = B2COrder.objects.update_or_create(
            external_id=external_id,
            defaults={
                "employer": employer,
                "order_name": lead_data.get("order_name"),
                "order_date": order_date,
                "order_time": order_time,
                "address": lead_data.get("address"),
                "phone_number_client": lead_data.get("phone"),
                "name_client": name_client,
                "price": lead_data.get("price"),
                "description": lead_data.get("description"),
                "city": city,
                "updated_at": updated_at,
            }
        )

        if created:
            logger.info(f"Новый заказ {lead_data['order_name']} успешно сохранен в базе данных.")
        else:
            logger.info(f"Заказ {lead_data['order_name']} был обновлен в базе данных.")
    except Exception as e:
        logger.error(f"Ошибка при обработке заказа {lead_data.get('order_name', 'without name')}: {e}")

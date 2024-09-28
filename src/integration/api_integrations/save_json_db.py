import json

from b2c_client_orders.models import B2COrder
from employers.models import Employer, Manager
from orders.models import City


def save_json_to_db(file_path="leads.json"):
    """Чтение данных из JSON файла и сохранение в базу данных."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            leads_data = json.load(file)
    except Exception as e:
        print(f"Ошибка при чтении файла {e}")
        return

    for lead_data in leads_data:
        try:
            # Проверяем наличие external_id
            external_id = lead_data.get("external_id")
            if not external_id:
                print(f"Пропущен заказ без external_id: {lead_data}")
                continue

            if B2COrder.objects.filter(external_id=external_id).exists():
                print(f"Заказ с external_id {external_id} уже существует в базе данных.")
                continue

            employer = Employer.objects.get(id=1)

            date_time = lead_data.get("date")
            if date_time and " " in date_time:
                order_date, order_time = date_time.split(" ")
            else:
                print(f"Неправильный формат даты: {date_time}")
                continue

            # Парсим имя клиента из контактов
            contacts = lead_data.get("contacts", [])
            name_client = contacts[0]["name"] if contacts else "Неизвестно"

            # Используем данные с уже сопоставленным городом для сохранения в БД
            city_name = lead_data["city"]["name"]
            country_name = lead_data["city"]["country"]

            city = City.objects.get(name=city_name, country__name=country_name)

            order = B2COrder(
                employer=employer,
                order_name=lead_data.get("order_name"),
                order_date=order_date,
                order_time=order_time,
                address=lead_data.get("address"),
                phone_number_client=lead_data.get("phone"),
                name_client=name_client,
                price=lead_data.get("price"),
                description="",
                city=city,
                external_id=external_id
            )

            # Сохраняем заказ в базу данных
            order.save()
            print(f"Заказ {lead_data['order_name']} успешно сохранен в базу данных.")
        except Exception as e:
            print(f"Ошибка при сохранении заказа {lead_data['order_name']}: {e}")

import json
from datetime import datetime
from django.utils import timezone

from b2c_client_orders.models import B2COrder
from employers.models import Employer
from integration.api_integrations.amo_integration import get_updated_leads
from orders.models import City
from amo_integration import save_leads_to_json

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

            # Проверяем, существует ли заказ с таким external_id
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
                    "description": "",
                    "city": city,
                    "updated_at": lead_data.get("updated_at"),
                }
            )

            if created:
                print(f"Новый заказ {lead_data['order_name']} успешно сохранен в базу данных.")
            else:
                print(f"Заказ {lead_data['order_name']} был обновлен в базе данных.")
        except Exception as e:
            print(f"Ошибка при обработке заказа {lead_data.get('order_name', 'без названия')}: {e}")

def update_leads_in_db():
    """Обновляем сделки в базе данных на основе текущих сделок."""
    leads = get_updated_leads()  # Получаем актуальные сделки из AmoCRM
    save_leads_to_json(leads)  # Сохраняем актуальные данные в JSON

    # Теперь читаем данные из JSON файла
    with open("leads.json", "r", encoding="utf-8") as file:
        leads_data = json.load(file)

    for lead_data in leads_data:
        try:
            external_id = lead_data.get("external_id")
            updated_at_api = timezone.make_aware(datetime.strptime(lead_data.get("updated_at"), "%Y-%m-%d %H:%M:%S"))

            # Получаем заказ из базы данных
            order = B2COrder.objects.filter(external_id=external_id).first()

            if order:
                # Сравниваем даты обновления
                if updated_at_api > order.updated_at:
                    print(f"Заказ {lead_data['order_name']} был изменен. Обновляем...")
                    update_order_in_db(order, lead_data)
                else:
                    print(f"Заказ {lead_data['order_name']} не изменен.")
            else:
                # Если заказа нет, создаем новый
                print(f"Новый заказ {lead_data['order_name']} добавлен.")
                create_new_order(lead_data)

        except Exception as e:
            print(f"Ошибка при обработке заказа {lead_data.get('order_name', 'без названия')}: {e}")

def update_order_in_db(order, lead_data):
    """Обновляем существующий заказ в базе данных."""
    city = City.objects.get(name=lead_data['city']['name'], country__name=lead_data['city']['country'])

    order.order_name = lead_data['order_name']
    order.price = lead_data['price']
    order.address = lead_data['address']
    order_date, order_time = lead_data['date'].split(' ')
    order.order_date = order_date
    order.order_time = order_time
    order.phone_number_client = lead_data['phone']
    order.city = city
    order.updated_at = timezone.make_aware(datetime.strptime(lead_data['updated_at'], "%Y-%m-%d %H:%M:%S"))
    order.save()
    print(f"Заказ {order.order_name} был обновлен.")

def create_new_order(lead_data):
    """Создаем новый заказ в базе данных."""
    city = City.objects.get(name=lead_data['city']['name'], country__name=lead_data['city']['country'])
    employer = Employer.objects.get(id=1)  # ID Компании для которого делается интеграция
    contacts = lead_data.get('contacts', [])
    name_client = contacts[0]['name'] if contacts else ""

    order_date, order_time = lead_data['date'].split(' ')

    B2COrder.objects.create(
        external_id=lead_data['external_id'],
        employer=employer,
        order_name=lead_data['order_name'],
        order_date=order_date,
        order_time=order_time,
        address=lead_data['address'],
        phone_number_client=lead_data['phone'],
        name_client=name_client,
        price=lead_data['price'],
        description="",
        city=city,
        updated_at=timezone.make_aware(datetime.strptime(lead_data['updated_at'], "%Y-%m-%d %H:%M:%S"))
    )
    print(f"Новый заказ {lead_data['order_name']} создан в базе данных.")

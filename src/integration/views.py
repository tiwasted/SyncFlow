import json
import logging
import re
import traceback
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from integration.api_integrations.save_lead import save_lead_to_db

logger = logging.getLogger(__name__)

def parse_key(key):
    return re.findall(r'\w+', key)

def recursive_set(data, keys, value):
    current = data
    for i, key in enumerate(keys):
        if key.isdigit():
            key = int(key)
        if i == len(keys) - 1:
            if isinstance(current, list):
                while len(current) <= key:
                    current.append(None)
                current[key] = value
            else:
                current[key] = value
        else:
            next_key = keys[i + 1]
            is_next_key_digit = next_key.isdigit()
            if isinstance(current, list):
                while len(current) <= key:
                    current.append({} if not is_next_key_digit else [])
                current = current[key]
            else:
                if key not in current:
                    current[key] = [] if is_next_key_digit else {}
                current = current[key]

def unix_to_datetime(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None

@csrf_exempt
def webhook_handler(request):
    """Webhook для работы с заказами в реальном времени."""
    if request.method == "POST":
        try:
            logger.info(f"Получено тело запроса: {request.body.decode('utf-8')}")
            payload = request.POST.dict()
            logger.info(f"Получен webhook с данными: {payload}")

            # Восстановление вложенной структуры данных
            nested_data = {}
            for key, value in payload.items():
                keys = parse_key(key)
                recursive_set(nested_data, keys, value)

            # Логируем восстановленные данные
            logger.debug(f"Восстановленные данные: {json.dumps(nested_data, ensure_ascii=False, indent=4)}")

            # Определяем, есть ли обновленные или добавленные сделки
            leads_data = nested_data.get('leads', {})
            event_type = None
            if 'update' in leads_data:
                event_type = 'update'
            elif 'add' in leads_data:
                event_type = 'add'
            else:
                logger.error("Не найдено ключей, относящихся к сделке")
                return JsonResponse({"error": "Нет данных о сделке в payload"}, status=400)

            lead_list = leads_data[event_type]
            if not isinstance(lead_list, list) or len(lead_list) == 0:
                logger.error("Список сделок пуст")
                return JsonResponse({"error": "Нет данных о сделке в payload"}, status=400)

            # Предполагаем, что обрабатываем первую сделку в списке
            lead = lead_list[0]

            # Логируем данные сделки
            logger.debug(f"Данные сделки: {json.dumps(lead, ensure_ascii=False, indent=4)}")

            # Извлекаем необходимые данные
            lead_id = lead.get("id")
            lead_name = lead.get("name")
            status_id = lead.get("status_id")

            if not lead_id or not status_id:
                logger.error("Отсутствует ID сделки или status_id")
                return JsonResponse({"error": "Отсутствует ID сделки или status_id"}, status=400)

            # Проверяем целевой статус
            TARGET_STATUS_ID = "44661403"  # Замените на ваш целевой ID статуса
            if str(status_id) != TARGET_STATUS_ID:
                logger.info(f"Сделка с ID {lead_id}, Название: {lead_name}, Статус ID: {status_id} не относится к целевому статусу. Игнорируем.")
                return JsonResponse({"status": "Игнорировано", "status_id": status_id}, status=200)

            # Обработка пользовательских полей
            custom_fields = lead.get('custom_fields', [])
            custom_fields_data = {}
            for field in custom_fields:
                field_name = field.get('name')
                field_values = field.get('values', [])
                if field_values:
                    if isinstance(field_values, list):
                        values = []
                        for v in field_values:
                            if isinstance(v, dict):
                                values.append(v.get('value') or v)
                            else:
                                values.append(v)
                        if len(values) == 1:
                            custom_fields_data[field_name] = values[0]
                        else:
                            custom_fields_data[field_name] = values
                    else:
                        custom_fields_data[field_name] = field_values

            # Обработка связанных контактов (если есть)
            contacts = []
            if 'contacts' in lead:
                for contact in lead['contacts']:
                    contact_info = {}
                    contact_info['id'] = contact.get('id')
                    contact_info['name'] = contact.get('name')
                    # Обработка пользовательских полей контакта, если есть
                    if 'custom_fields' in contact:
                        for field in contact['custom_fields']:
                            field_name = field.get('name')
                            field_values = field.get('values', [])
                            if field_values:
                                if len(field_values) > 1:
                                    contact_info[field_name] = [v.get('value') for v in field_values]
                                else:
                                    contact_info[field_name] = field_values[0].get('value')
                    contacts.append(contact_info)

            # Преобразование временных меток в даты
            created_at = unix_to_datetime(lead.get("created_at"))
            updated_at = unix_to_datetime(lead.get("updated_at"))

            # Обработка города
            city_name = custom_fields_data.get("Какой город")
            city = None
            if city_name:
                city = {
                    "name": city_name,
                    "country": "Казахстан"  # Замените на соответствующую страну или извлеките из данных
                }

            # Формируем структуру данных для сохранения
            lead_data_to_save = {
                "external_id": int(lead_id),
                "order_name": lead_name,
                "price": int(lead.get("price")) if lead.get("price") else None,
                "address": custom_fields_data.get("Адрес проведения работ"),
                "date": unix_to_datetime(custom_fields_data.get("Дата и время проведения работ")),
                "phone": custom_fields_data.get("Телефон для API"),
                "city": city,
                "description": custom_fields_data.get("ОПИСАНИЕ ЗАКАЗА"),
                "updated_at": updated_at,
                "contacts": contacts if contacts else None
            }

            # Логируем информацию о событии
            logger.info(f"Событие {event_type} лида. Название: {lead_name}, ID сделки: {lead_id}, Статус ID: {status_id}")

            # Сохраняем данные
            save_lead_to_db(lead_data_to_save)

            return JsonResponse({"status": "Успешно", "status_id": status_id}, status=200)

        except Exception as e:
            logger.error(f"Ошибка при обработке запроса: {e}\n{traceback.format_exc()}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Разрешен только метод POST"}, status=405)

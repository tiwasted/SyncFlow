import os
import sys
import django

project_root = '/app/src'
sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "syncflow.settings")

django.setup()

from amocrm.v2 import tokens, Lead as _Lead, custom_field, filters
from amocrm.v2 import Pipeline, Status
from amocrm.v2.tokens import default_token_manager

import json
import logging
from dotenv import load_dotenv
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from orders.models import Country, City

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))


class CustomLead(_Lead):
    """Кастомный класс для работы с кастомными полями DezCity."""
    address = custom_field.TextCustomField("Адрес проведения работ")
    date = custom_field.DateTimeCustomField("Дата и время проведения работ")
    phone = custom_field.TextCustomField("Телефон для API")
    city = custom_field.TextCustomField("Какой город")

def init_amo_tokens():
    """Инициализация токенов для работы с API AmoCRM."""
    logger.info("Начало инициализации токенов")
    tokens.default_token_manager(
        client_id=(os.getenv("AMOCRM_CLIENT_ID")),
        client_secret=(os.getenv("AMOCRM_CLIENT_SECRET")),
        subdomain=(os.getenv("AMOCRM_SUBDOMAIN")),
        redirect_url=(os.getenv("AMOCRM_REDIRECT_URL")),
        storage=tokens.FileTokensStorage(directory_path=current_dir),  # by default FileTokensStorage
    )
    logger.info("Токены успешно инициализированы")

def get_leads_in_first_stage_process():
    """Получаем заказы из статуса "1 этап обработки" """
    pipeline_id = os.getenv("PIPELINE_ID")
    status_id = os.getenv("STATUS_ID")

    leads_in_stage_filter = filters.FiltersByPipelineAndStatus("statuses")
    leads_in_stage_filter(pipline_id=pipeline_id, status_id=status_id)
    return CustomLead.objects.filter(filters=(leads_in_stage_filter,))

CITY_MAPPING = {
    "Алмата": "Алматы",
}

def normalize_city_name(city_name):
    """Возвращает нормализованные название городов."""
    city_name = city_name.strip()
    return CITY_MAPPING.get(city_name, city_name)

def process_city(city_name):
    """Обрабатывает название города и возвращает объект города, если город существует."""
    normalized_city_name = normalize_city_name(city_name)

    try:
        # Пока страна Казахстан. В дальнейшим лучше передавать параметром.
        country_name = "Казахстан"
        country = Country.objects.get(name=country_name)
        city = City.objects.get(name=normalized_city_name, country=country)
        return city
    except ObjectDoesNotExist:
        print(f"Город ''{city_name} не найден в базе.")
        return None

def save_leads_to_json(leads, file_path="leads.json"):
    """Сохраняем заказы в JSON файл."""
    leads_data = []
    for lead in leads:
        # Проверяем наличие города
        city = process_city(lead.city)
        if city:
            # Если город найден, сохраняем его
            lead_data = {
                "order_name": lead.name,
                "price": lead.price,
                "address": lead.address,
                "date": str(lead.date),
                "phone": lead.phone,
                "city": {"name": city.name, "country": city.country.name},
                "external_id": lead.id,
                "contacts": [{"name": contact.name} for contact in lead.contacts],
                "updated_at": str(lead.updated_at),
            }
            leads_data.append(lead_data)
        else:
            print(f"Заказ с городом '{lead.city}' пропущен.")

    # Записываем в JSON файл
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(leads_data, file, ensure_ascii=False, indent=4)
    print(f"Данные сохранены в файл {file_path}")

def get_updated_leads():
    """Получаем все актуальные сделки из AmoCRM."""
    init_amo_tokens()
    return get_leads_in_first_stage_process()


if __name__ == "__main__":
    init_amo_tokens()
    leads = get_leads_in_first_stage_process()
    save_leads_to_json(leads)

    from save_json_db import save_json_to_db, update_leads_in_db
    save_json_to_db()
    update_leads_in_db()


    # for index, lead in enumerate(leads, start=1):
    #     print(f"{index}.")
    #     print(f"ID: {lead.id}")
    #     print(f"Наименование: {lead.name}")
    #     print(f"Бюджет: {lead.price}")
    #     print(f"Адрес: {lead.address}")
    #     print(f"Дата и время: {lead.date}")
    #     print(f"Телефон: {lead.phone}")
    #     print(f"Город: {lead.city}")
    #     print(f"Дата изменения сделки: {lead.updated_at}")
    #
    #     for contact in lead.contacts:
    #         print(f"Контакт: {contact.name}")
    #     print("------")

    # Сначала нужно получить ID воронки и статуса, чтобы получить сделки с определенного статуса.

    # pipelines = Pipeline.objects.all()
    # for pipeline in pipelines:
    #     print(pipeline.name, pipeline.id)
    #
    #     pipeline_id = os.getenv("PIPELINE_ID")
    #
    #     statuses_manager = Status.get_for(pipeline_id)
    #
    #     statuses = statuses_manager.all()

        # for status in statuses:
        #     print(status.name, status.id)

        # statuses = Pipeline.objects.filter(pipeline_id=pipeline.id)
        # for status in statuses:
        #     print(status.name, status.id)

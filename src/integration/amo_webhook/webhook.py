import requests
import os
import logging
from integration.amo_webhook.auth_utils import _get_access_token

logger = logging.getLogger(__name__)

def register_webhook():
    """
    Регистрация webhook в amoCRM для событий создания и обновления сделок.
    """
    amocrm_subdomain = os.getenv('AMOCRM_SUBDOMAIN')
    access_token = _get_access_token()
    webhook_url = "https://e09a-2-133-56-84.ngrok-free.app/orders/webhook/"

    # URL для регистрации webhooks в amoCRM
    url = f"https://{amocrm_subdomain}.amocrm.ru/api/v4/webhooks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "destination": webhook_url,
        "settings": ["add_lead", "update_lead"]
    }

    # Отправляем запрос для регистрации webhook
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        logger.info("Webhook успешно зарегистрирован.")
        logger.info(f"Ответ от сервера: {response.json()}")
    else:
        logger.error(f"Ошибка регистрации Webhook. Код статуса: {response.status_code}, Ответ: {response.text}")

# Вызов функции регистрации webhook
register_webhook()

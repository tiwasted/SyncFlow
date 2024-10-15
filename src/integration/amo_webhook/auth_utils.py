import jwt
import os
import requests
import dotenv
import logging

from dotenv import load_dotenv
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))

subdomain = os.getenv("AMOCRM_SUBDOMAIN")
client_id = os.getenv("AMOCRM_CLIENT_ID")
client_secret = os.getenv("AMOCRM_CLIENT_SECRET")
redirect_uri = os.getenv("AMOCRM_REDIRECT_URL")
secret_code = os.getenv("AMOCRM_SECRET_CODE")


def _is_expire(token: str):
    token_data = jwt.decode(token, options={"verify_signature": False})
    exp = datetime.fromtimestamp(token_data["exp"], tz=timezone.utc)
    now = datetime.now(timezone.utc)
    return now >= exp


def _save_tokens(access_token: str, refresh_token: str):
    # Переменные окружения
    os.environ["AMOCRM_ACCESS_TOKEN"] = access_token
    os.environ["AMOCRM_REFRESH_TOKEN"] = refresh_token

    dotenv_path = os.path.join(current_dir, '.env')

    # Запись токенов в .env файл
    dotenv.set_key(dotenv_path, "AMOCRM_ACCESS_TOKEN", os.environ["AMOCRM_ACCESS_TOKEN"])
    dotenv.set_key(dotenv_path, "AMOCRM_REFRESH_TOKEN", os.environ["AMOCRM_REFRESH_TOKEN"])


def _get_refresh_token():
    return os.getenv("AMOCRM_REFRESH_TOKEN")


def _get_access_token():
    access_token = os.getenv("AMOCRM_ACCESS_TOKEN")

    if not access_token:
        logger.error("Токен доступа отсутствует. Запустите процесс авторизации.")
        raise ValueError("Токен доступа отсутствует.")

    if _is_expire(access_token):
        logger.info("Срок действия токена истек, получаем новый.")
        _get_new_tokens()  # Попытка получить новый токен
        access_token = os.getenv("AMOCRM_ACCESS_TOKEN")

    if not access_token:
        logger.error("Не удалось обновить токен доступа. Проверьте процесс авторизации.")
        raise ValueError("Не удалось обновить токен доступа.")

    return access_token


def _get_new_tokens():
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": _get_refresh_token(),
        "redirect_uri": redirect_uri
    }

    response = requests.post(f"https://{subdomain}.amocrm.ru/oauth2/access_token", json=data).json()

    if response.status_code != 200:
        logger.error(f"Ошибка получения нового токена: {response.text}")
        raise ValueError(f"Не удалось получить новый токен доступа. Ответ сервера: {response.text}")

    response_data = response.json()
    access_token = response["access_token"]
    refresh_token = response["refresh_token"]

    if not access_token or not refresh_token:
        logger.error(f"Ошибка в ответе при обновлении токена: {response_data}")
        raise ValueError("Ошибка в ответе при обновлении токена.")

    _save_tokens(access_token, refresh_token)

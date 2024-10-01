from amocrm.v2 import tokens
import os
from dotenv import load_dotenv


load_dotenv()

def init_amo_tokens():
    # Создаем менеджер токенов
    token_manager = tokens.default_token_manager(
        client_id=os.getenv("AMOCRM_CLIENT_ID"),
        client_secret=os.getenv("AMOCRM_CLIENT_SECRET"),
        subdomain=os.getenv("AMOCRM_SUBDOMAIN"),
        redirect_url=os.getenv("AMOCRM_REDIRECT_URL"),
        storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
    )

    if not token_manager.is_access_token_valid():
        print("Токены отсутствуют или истекли. Начинаем процесс авторизации.")
        print("Перейдите по следующей ссылке и авторизуйтесь:")
        print(token_manager.get_authorization_url())
        code = input("Введите полученный код авторизации: ")
        token_manager.init(code)
        print("Токены успешно инициализированы и сохранены.")
    else:
        print("Токены действительны.")

if __name__ == "__main__":
    init_amo_tokens()

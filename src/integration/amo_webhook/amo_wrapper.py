import os
import requests

from dotenv import load_dotenv

from integration.amo_webhook.auth_utils import _save_tokens

load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))

subdomain = os.getenv("AMOCRM_SUBDOMAIN")
client_id = os.getenv("AMOCRM_CLIENT_ID")
client_secret = os.getenv("AMOCRM_CLIENT_SECRET")
redirect_uri = os.getenv("AMOCRM_REDIRECT_URL")
secret_code = os.getenv("AMOCRM_SECRET_CODE")


class AmoCRMWrapper:
    def init_oauth2(self):
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": secret_code,
            "redirect_uri": redirect_uri
        }

        response = requests.post("https://{}.amocrm.ru/oauth2/access_token".format(subdomain), json=data).json()
        print(response)
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]

        _save_tokens(access_token, refresh_token)

amocrm_wrapper_1 = AmoCRMWrapper()

# amocrm_wrapper_1.init_oauth2()

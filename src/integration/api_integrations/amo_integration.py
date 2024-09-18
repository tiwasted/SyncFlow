from amocrm.v2 import tokens, Lead as _Lead, custom_field, filters
from amocrm.v2 import Pipeline, Status
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    # Создаем менеджер токенов
    tokens.default_token_manager(
        client_id=(os.getenv("AMOCRM_CLIENT_ID")),
        client_secret=(os.getenv("AMOCRM_CLIENT_SECRET")),
        subdomain=(os.getenv("AMOCRM_SUBDOMAIN")),
        redirect_url=(os.getenv("AMOCRM_REDIRECT_URL")),
        storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
    )

    """
    Сначала нужно получить ID воронки и статуса, чтобы получить сделки с определенного статуса.
    """
    # pipelines = Pipeline.objects.all()
    # for pipeline in pipelines:
    #     print(pipeline.name, pipeline.id)
    #
    #     pipeline_id = 4941127
    #
    #     statuses_manager = Status.get_for(pipeline_id)
    #
    #     statuses = statuses_manager.all()

        # for status in statuses:
        #     print(status.name, status.id)

        # statuses = Pipeline.objects.filter(pipeline_id=pipeline.id)
        # for status in statuses:
        #     print(status.name, status.id)

    class CustomLead(_Lead):
        """Кастомный класс для работы с кастомными полями."""
        phone = custom_field.ContactPhoneField("Раб. тел.")
        address = custom_field.TextCustomField("Адрес")
        other = custom_field.TextCustomField("Другой")

    pipeline_id = (os.getenv("PIPELINE_ID")) # ID воронки
    status_id = (os.getenv("STATUS_ID"))     # ID статуса

    leads_in_stage_filter = filters.FiltersByPipelineAndStatus("statuses")
    leads_in_stage_filter(pipline_id=pipeline_id, status_id=status_id)
    leads = CustomLead.objects.filter(filters=(leads_in_stage_filter,))

    for index, lead in enumerate(leads, start=1):
            print(f"{index}.  Name: {lead.name}")
            print(f"Price: {lead.price}")
            for contact in lead.contacts:
                print(f"Contact: {contact.name}")
            print(f"Phone: {lead.other}")
            print(f"Phone: {lead.phone}")
            print(f"Address: {lead.address}")

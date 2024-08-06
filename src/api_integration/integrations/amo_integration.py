from amocrm.v2 import tokens, Lead as _Lead, Pipeline, Contact, Company, custom_field


if __name__ == '__main__':
    tokens.default_token_manager(
        client_id="d89cd82a-44a1-429d-af4c-0fffcf7c76b6",
        client_secret="NPQOAws5ys6F2OG0rbTDR8xWRxrLmKu7aHjse3UqHgGINyzZf40oHrXYbx9PRU5s",
        subdomain="mkrgkz",
        redirect_url="https://yandex.kz/",
        storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
    )

    # tokens.default_token_manager.init(code="def50200292178d7604d64a2074f0b419e678408cd7370d4866f25dce4a6016e37fd5d124ee318ac25c0ac67c95307e07cc45022d16941c4e7e05f2dc2876a44a08636b573fcc64c78923154a9ff3218a7964e5285889df4f8be8068ec2caffd231eebe86ff4ff1577478d66812ab6ef49f0fa3729f76a5815add2258fc1a288fd3e5860ba40afbf53cf79484405a3fa5c4c433d298cb909fdeeac82c4413d9287171696d8fe7eddb17f06c870da78a3b0eaa0a5eaba476c3b36224de27b84679f667bc7ddbce9a596b8329a31285324d4fd5858f6e5dd04071299b1259ed4487e62d66397cd99557d245f31ff1f24daae39664a1e8165e3bee35b6d6a8a1154ae4363f8b8132fc794b3e189f0d42ec57e08533bee9df975e6c9d555dcec7ee5c908da13f263da93363c21001c00a61e0cd80c44e633fc16762b48c1a1b69d6a2614530486ea1a0e208079cff1292cdbf026dfdb520f9297913b733d76933093f12417d087ab288c778264a8b390b018c42c36ace628de81ed00fb9ac5c0510184ce624e095367013311ef47a06c93a49e71edafc5c3d748cc4a657c0c0d482b517096b2a210ae236e28a9dde40e19bdeb239c25c6a4647986e12ed9ad583fd806450563c1c47f26f25000f9ba5aa60e48f73f38d3ab54be14c1c0011044bc7d56b58fbb",
    #                                 skip_error=False)

    # lead = Lead.objects.get(query="первый этап")
    # print(lead.name, lead.price, lead.id, lead.contacts)

    # class CustomLead(_Lead):
    #     # phone = custom_field.TextCustomField("Раб. тел.")
    #     address = custom_field.TextCustomField("Адрес")
    #
    # leads = CustomLead.objects.all()
    # for lead in leads:
    #
    #     print(lead.name)
    #     print(lead.price)
    #
    #     contacts_list = list(lead.contacts)
    #     for contact in contacts_list:
    #         print(contact.name)
    #
    #     print(lead.address)



    # for lead in leads:



    # contacts = Contact.objects.all()
    # for contact in contacts:
    #     print(contact.name)



    # companies = Company.objects.all()
    #
    # for company in companies:
    #     contacts_list = list(company.contacts)  # Преобразуем ленивый объект в список
    #
    #     for contact in contacts_list:
    #         contact_data = contact._data  # Получаем данные контакта
    #         contact_name = contact_data.get('name', 'Имя не найдено')
    #         contact_contacts = contact_data.get('customers', 'Номер телефона не найден')
    #
    #         print(f"Контакт: {contact_name}, Телефон: {contact_contacts}")


    class CustomLead(_Lead):
        # Определяем кастомное поле с указанием ID и под ID
        phone = custom_field.TextCustomField("Раб. тел.")
        address = custom_field.TextCustomField("Адрес")

    # Получаем объект типа CustomLead
    lead = CustomLead.objects.get(query='первый этап')

    # Вывод стандартных полей
    print(f"Name: {lead.name}")
    print(f"Price: {lead.price}")
    print(lead.contacts)
    print(f"Name: {lead.name}")
    print(f"Price: {lead.price}")
    print(f"Phone: {lead.phone}")
    print(f"Address: {lead.address}")

    # Вывод кастомного поля
    print(f"Phone: {lead.phone}")
    #
    # # Вывод всех атрибутов объекта lead для диагностики
    # print("\nAll attributes and their values:")
    # for attr in dir(lead):
    #     if not attr.startswith("_"):
    #         try:
    #             print(f"{attr}: {getattr(lead, attr)}")
    #         except AttributeError:
    #             print(f"{attr}: Attribute not found")

































# from amocrm_api import AmoLegacyClient # for login password auth
# from amocrm_api import AmoOAuthClient # for oauth
# from datetime import datetime
#
# client = AmoLegacyClient('mkrg_kz@mail.ru', 'hniwqPFV', 'https://mkrgkz.amocrm.ru/')
# client = AmoOAuthClient('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjcxM2EzZDRhZTMzYWJkNTdmMzc2YThjZThjMDNkMDdjY2JmNmFkMzAwZjYwYWU4MDA4ZWRmNTMxOTRjMmNmOTU5OGUwYWE0ZjM4OTAxMzExIn0.eyJhdWQiOiI4ZWQ4NTQ2NC1iOGY5LTRiZTgtYjkwYi1kYTk2MGQzNjViY2YiLCJqdGkiOiI3MTNhM2Q0YWUzM2FiZDU3ZjM3NmE4Y2U4YzAzZDA3Y2NiZjZhZDMwMGY2MGFlODAwOGVkZjUzMTk0YzJjZjk1OThlMGFhNGYzODkwMTMxMSIsImlhdCI6MTcyMjYxNjAxMiwibmJmIjoxNzIyNjE2MDEyLCJleHAiOjE3MjI3MDI0MTIsInN1YiI6IjExMzQ1NTY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxODc5NTM0LCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiMzM0Y2ZlOTUtMDg1Zi00NWZjLTlmYzctNWViZmUxNGQ4ZmY1In0.KkmUsLd44_9c2PpsUu3_FsWwXdwEOMPA-MVSXt2vnbTKYyi4zsA1zzq92W6VrQxEzGTzlQGUkWnRaGLNzKdzbjJfjKFQsBK2SNfKy4fih8Vo_fuIsUUHBsfz8ut8gHW05c9KIHHC_q91MAUT-y48psDtSFY09iT7lmyUPFKDEkRy8Xrkq1CBjbZPA8L5n8nuvA0hsuw17VvgG_HUzUz4NYJiOZTKXhjERfs4WJHM6nUv0hH5eI_2z6B2OK_TLQwbX_gP864mB35BhR1SDa39b30M4gBNAhrSLsze3N4rvJjHwZW_CS4fM1V7aHT4e5FaTQe7m06TAmqTUfA0mMyI-w',
#                         'def5020064b0640079ac3f3befebe369ab2cae74dfa2860c999f59bc3a4b7c421c76d1eaca83aed455087d7d530ee2960e5a5be3602fc0c0c2852d488f42c56562d752060f165d72db7c02b514f20b47c2051b378c8a4900b241b29d2e55ab64a6bb8d1c11f00168ee6054b24a58520d44ac50dd5355f397161c099224abdcff0e0872391d65a4d251a93da2a42a5af7e2c33aa6a5758e7a407b6dfe20974fb6c0d635c294d8225adf5eb1b1586040d00307fd20e12c94434441acd44e2cb8667fe65be4e819507182e9be662c263cc1fa915d5866f6428e5c6225e5f961d3844c78a729851d84d4e320c6c14ba9345a22c9a8d7f9cff1c3326a605e6f9b4b87493e5268956d3f9866f6562231129f3eb44110d823fd0fecc98573a120c28d9439c93beeee67a0d009a76c1719a6e8f1cad3b26e90cd6a710fe1a97fa713e76b5563407be5cb9e6271dcd65d2b2c7f67cd1024308c213eec01bbf7e91db30d86d60c47fa39d5a6749db2586b0f3073ea6300a7763e6e1803ab3ad8448f1be5236bfbe45b00021cb8f85eadfa260ff768f6ea2e06d0edd9ccc723f1e3109dabc41ef97a453889206e371f83c92ebb985b12eb66453f775f43d182e2c337a0e28bd54ef7e4302dffbd625aab36c363729c1e25880820b85af4fcd531d186a6513eadaf984879c258ca39511e3311fe',
#                         'https://mkrgkz.amocrm.ru/',
#                         '8ed85464-b8f9-4be8-b90b-da960d365bcf',
#                         'XAEUkjDTtzYCSE8aPeKfnbCdH2HigFPEw6EsMifNZmTznaXBrT3dGB6HEoxm5g5M', 'https://yandex.kz/')
# dt = datetime.datetime.today().strftime("%a, %d %b %Y %H-%m-%d")
# date_time = f"{dt} UTC"
#
# # for Legacy client
# headers = {
#     "IF-MODIFIED-SINCE": f"{date_time}",
#     "Content-Type": "application/json",
# }
#
# client.update_session_params(headers)
#
# lead = client.get_lead()
# print(lead)

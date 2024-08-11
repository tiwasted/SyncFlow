# from amocrm.v2 import tokens, Lead as _Lead, Pipeline, Contact, Company, custom_field
#
#
# if __name__ == '__main__':
#     tokens.default_token_manager(

#         subdomain="mkrgkz",
#         redirect_url="https://yandex.kz/",
#         storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
#     )



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


    # class CustomLead(_Lead):
    #     # Определяем кастомное поле с указанием ID и под ID
    #     phone = custom_field.TextCustomField("Раб. тел.")
    #     address = custom_field.TextCustomField("Адрес")
    #
    # # Получаем объект типа CustomLead
    # lead = CustomLead.objects.get(query='первый этап')
    #
    # # Вывод стандартных полей
    # print(f"Name: {lead.name}")
    # print(f"Price: {lead.price}")
    # print(lead.contacts)
    # print(f"Name: {lead.name}")
    # print(f"Price: {lead.price}")
    # print(f"Phone: {lead.phone}")
    # print(f"Address: {lead.address}")
    #
    # # Вывод кастомного поля
    # print(f"Phone: {lead.phone}")
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

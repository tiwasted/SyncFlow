from datetime import datetime
from b2c_client_orders.models import B2COrder
from integration.api_integrations.amo_integration import init_amo_tokens, get_leads_in_first_stage_process
from functools import wraps


# def initialize_amo_tokens(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         init_amo_tokens()
#         return func(*args, **kwargs)
#
#     return wrapper


# @initialize_amo_tokens
# class AmoCRMIntegration:
#     @staticmethod
#     def sync_with_external_api():
#         init_amo_tokens()
#
#         leads = get_leads_in_first_stage_process()
#
#         # Обработка каждого лида
#         for lead in leads:
#             if lead.date:
#                 datetime_obj = datetime.strptime(str(lead.date), "%Y-%m-%d %H:%M:%S")
#                 order_date = datetime_obj.date()
#                 order_time = datetime_obj.time()
#             else:
#                 order_date = None
#                 order_time = None
#
#             B2COrder.objects.update_or_create(
#                 external_id=lead.id,
#                 defaults={
#                     'order_name': lead.name,
#                     'price': lead.price,
#                     'address': lead.address,
#                     'order_date': lead.date.date() if lead.date else None,
#                     'order_time': lead.date.time() if lead.date else None,
#                     'phone_number_client': lead.phone,
#                     'description': getattr(lead, 'description', ''),
#                     'status': 'in_processing',
#                 }
#             )

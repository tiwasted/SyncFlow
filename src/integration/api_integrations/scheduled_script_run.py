from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

from amo_integration import init_amo_tokens, get_leads_in_first_stage_process, save_leads_to_json
from integration.api_integrations.save_lead import save_json_to_db, update_leads_in_db

logging.basicConfig(level=logging.INFO)

def scheduled_job():
    try:
        logging.info("Инициализация токенов AmoCRM")
        init_amo_tokens()

        logging.info("Получение сделок из первой стадии")
        leads = get_leads_in_first_stage_process()

        logging.info("Сохранение сделок в JSON")
        save_leads_to_json(leads)

        logging.info("Сохранение сделок в БД")
        save_json_to_db()

        logging.info("Обновление сделок в БД")
        update_leads_in_db()

        logging.info("Задача успешно выполнена")
    except Exception as e:
        logging.error(f"Ошибка при выполнении задачи: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(
        scheduled_job,
        trigger=IntervalTrigger(hours=1),
        next_run_time=None,
        id='update_leads',
        name='Обновление сделок из AmoCRM',
        max_instances=1,
        coalesce=True  # Объединяет пропущенные запуски в один
    )

    try:
        logging.info("Планировщик запущен")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Планировщик остановлен")

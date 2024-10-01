from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

from amo_integration import init_amo_tokens, get_leads_in_first_stage_process, save_leads_to_json, save_json_to_db, update_leads_in_db

logging.basicConfig(level=logging.INFO)

def scheduled_job():
    try:
        init_amo_tokens()
        leads = get_leads_in_first_stage_process()
        save_leads_to_json(leads)
        save_json_to_db()
        update_leads_in_db()
        logging.info("Задача успешно выполнена")
    except Exception as e:
        logging.error(f"Ошибка при выполнении задачи: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(
        scheduled_job,
        trigger=IntervalTrigger(hours=1),
        next_run_time=None,  # None означает, что первый запуск произойдет через 3 часа
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

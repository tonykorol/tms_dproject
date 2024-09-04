import asyncio
import logging
from datetime import timedelta

from celery.signals import after_setup_logger

from celery import Celery

from config import REDIS_HOST, REDIS_PORT
from scrappers.notifications.tg.tg import update_user_tg_ids
from scrappers.run import run

celery = Celery("tasks", broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/")

celery.conf.update(
    timezone="UTC",
    enable_utc=True,
    worker_hijack_root_logger=False,
    broker_connection_retry_on_startup=True,
)

logger = logging.getLogger(__name__)


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh = logging.FileHandler("logs.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


loop = asyncio.get_event_loop()


@celery.task
def run_upd_tg():
    result = loop.run_until_complete(update_user_tg_ids())
    return result


@celery.task
def run_parse():
    result = loop.run_until_complete(run())
    return result


celery.conf.beat_schedule = {
    "run_upd_tg": {
        "task": "worker.worker.run_upd_tg",
        "schedule": timedelta(hours=1),  # Every 1 hour
    },
    "run_parse": {
        "task": "worker.worker.run_parse",
        "schedule": timedelta(hours=1),  # Every 1 hour
    },
}

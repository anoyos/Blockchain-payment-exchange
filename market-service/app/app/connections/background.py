from typing import Any

from api_contrib.core.utils import logger
from celery import Celery

from app.core.config import settings

celery_app = Celery("worker",
                    broker=settings.CELERY_BROKER_URL,
                    backend=settings.CELERY_BACKEND_URL)

celery_app.conf.update({
    'task_routes': {
        settings.UPDATE_QUOTES_TASK: {'queue': 'quotes', 'routing_key': 'quotes.update'}
    }
})


def send_message(message: Any, task_name: str, wait_result=True) -> dict:
    """ Send task to queue """
    data = {'status': 'not executed'}
    if message:
        # TODO: refactor it
        arg_name = "trade" if task_name == settings.UPDATE_QUOTES_TASK else "message"
        result = celery_app.send_task(task_name,
                                      kwargs={arg_name: message})

        logger.info(f"Send {task_name} to external service")
        if wait_result:
            data = result.get()
            logger.info(f"{task_name} status: {data['status']}")
        else:
            data = {'status': 'task sent'}
    return data

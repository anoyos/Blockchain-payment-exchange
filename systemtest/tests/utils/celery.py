from uuid import uuid4

from celery import Celery
from celery.app.log import TaskFormatter
from celery.signals import after_setup_logger



def make_celery(**kwargs):
    """
    :param app_name:
    :param redis_url:
    :param redis_db:
    :param mq_url:
    :param kwargs:
    task_queues: tuple of queues to be created by celery
    task_create_missing_queues: boolean to regulate if celery gets to create queue
    :return:
    """

    celery = Celery(
        "the-system-tests",
        backend="redis://:my_master_password@redis-master:6379/15",
        broker="amqp://guest:guest@rabbitmq:5672",
    )

    task_queues = None
    if 'task_queues' in kwargs:
        task_queues = kwargs['task_queues']

    task_create_missing_queues = True
    if 'task_create_missing_queues' in kwargs:
        task_create_missing_queues = kwargs['task_create_missing_queues']

    celery.conf.update(
        result_backend_transport_options={
            "socket_keepalive": True,
            "retry_on_timeout": True,
        },
        redis_retry_on_timeout=True,
        redis_socket_keepalive=True,
        timezone="Europe/Stockholm",
        task_create_missing_queues=task_create_missing_queues,
        task_queues=task_queues,
        enable_utc=True,
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        broker_heartbeat=None,
        event_queue_expires=60,
        worker_send_task_events=True,
        broker_connection_timeout=30,
    )

    return celery

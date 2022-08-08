from celery import Celery

from app.core.config import settings


celery_app = Celery("worker",
                    broker=settings.CELERY_BROKER_URL,
                    backend=settings.CELERY_BACKEND_URL)

celery_app.conf.update({
    'task_routes': {
        'app.worker.apply_blockchain_transaction': {'queue': 'blockchain'}
    }
})
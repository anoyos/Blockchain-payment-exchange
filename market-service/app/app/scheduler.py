import logging

from api_contrib.core.utils import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from prometheus_client.exposition import start_http_server

from app.tasks.jobs import robot

logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.info("Start app scheduler")
    start_http_server(80)

    scheduler = BlockingScheduler()

    scheduler.add_job(robot.create_orders, trigger='cron', second='*/10')

    scheduler.start()

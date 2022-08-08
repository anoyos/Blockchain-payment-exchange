import logging
from time import sleep

from api_contrib.core.utils import logger

from app.tasks.jobs import robot

logger.setLevel(logging.INFO)

if __name__ == '__main__':
    while True:
        robot.create_orders()
        sleep(10)

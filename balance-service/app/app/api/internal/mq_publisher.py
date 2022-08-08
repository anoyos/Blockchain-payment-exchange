import logging

from api_contrib.core.mq import Publisher

logging.getLogger("pika").setLevel(logging.WARNING)
publisher = Publisher()
publisher.connect()

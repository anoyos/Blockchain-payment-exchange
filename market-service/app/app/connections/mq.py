import logging
from json import dumps

from api_contrib.core.mq import Publisher
from api_contrib.core.utils import CustomEncoder
from api_contrib.core.utils import logger

logging.getLogger("pika").setLevel(logging.WARNING)


class MyPublisher(Publisher):

    def send_event(self, event: str, data: dict, room: str = None) -> None:
        logger.info(f"send {event}")
        message = {
            "event_name": event,
            "data": data
        }
        if room is not None:
            message.update({
                "room": room
            })
        self.publish(bytes(dumps(message, cls=CustomEncoder), 'utf-8'))


publisher = MyPublisher()
publisher.connect()

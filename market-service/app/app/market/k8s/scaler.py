from os import getenv
from time import sleep
from datetime import datetime
import redis
from api_contrib.core.utils import logger

from app import crud
from app import models
from app.core.config import settings
from app.core.constants import MARKETS_BY_SYMBOL
from app.market.k8s import tools

redis = redis.client.Redis(host=settings.REDIS_URL, password=settings.REDIS_PASS)


def redis_subscribe(symbol: str) -> bool:
    """ Subscribe on key if number of subscribers is 0 """
    if redis.pubsub_numsub(symbol)[0][1] == 0:
        sub = redis.pubsub()
        sub.subscribe(symbol)
        return True

    return False


def _log_redis_channels():
    for num, symbol in enumerate(MARKETS_BY_SYMBOL, start=1):
        subs_num = redis.pubsub_numsub(symbol)[0][1]
        logger.info(f"Redis pub/sub {num}: {symbol} = {subs_num}")


def _reserve_symbol_for_handle() -> str:
    """
    Use Redis pub/sub to map trading pairs for process
    Key feature here is that pod cancel subscription when died
    """
    subscribed = False
    start_wait_time = datetime.now()
    logger.info("Try to subscribe on symbol")
    while not subscribed:
        for symbol in MARKETS_BY_SYMBOL:
            subscribed = redis_subscribe(symbol)
            if subscribed:
                logger.info(f"Subscribe on {symbol}, wait_time: {datetime.now() - start_wait_time}")
                return symbol
        sleep(3)


def _wait_pod_status(pod_name):
    """ Wait pod for `Running` status Wait pod for `Running` status """
    running = tools.is_pod_running(pod_name)
    while not running:
        logger.info("Wait pod for Running status")
        sleep(3)
        running = tools.is_pod_running(pod_name)


def create_process_for_market() -> models.Market:
    # Clear markets executor list
    pod_name = getenv("POD_NAME")

    # Reserve symbol in redis
    symbol = _reserve_symbol_for_handle()

    market_obj = crud.market.find_one_sync({"symbol": symbol}, return_obj=True)
    crud.market.update_obj_sync(market_obj, {"executor": pod_name})

    # Scale pods if need
    tools.scale_broker_pods(desire_size=len(MARKETS_BY_SYMBOL), force=True)

    # Log redis channel only for debug purpose
    _log_redis_channels()

    return market_obj

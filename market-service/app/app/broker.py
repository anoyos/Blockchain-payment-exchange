from prometheus_client import start_http_server

from app.market.core.broker import MarketBroker
from app.market.k8s import scaler


def main():
    start_http_server(80)

    broker = MarketBroker(market=scaler.create_process_for_market())
    broker.start()


if __name__ == '__main__':
    main()

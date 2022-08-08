from bullflag_commons import get_mq_url
from bullflag_commons.containers.containers import BullflagAbstractFlaskContainer
from bullflag_commons.crypto import TokenService
from bullflag_commons.flask.flask_application import FlaskApplication
from bullflag_commons.redisinterface import RedisInterface, get_redis_url
from bullflag_connector_dummies.make_celery import make_celery
from bullflag_connector_dummies.queue_definitions import MARKET_QUEUE, TOKEN_QUEUE, WALLET_QUEUE, TOKEN_QUEUE_NAME, \
    TROLLBOX_QUEUE
from bullflag_connector_dummies.v2.market import MarketCeleryProducer
from bullflag_connector_dummies.v2.token import TokenCeleryProducer
from bullflag_connector_dummies.v2.trollbox import TrollboxCeleryProducer
from bullflag_connector_dummies.v2.wallet import WalletCeleryProducer
from dependency_injector import providers
from flask_restful import Api
from redis import Redis

from app.routes import RoutesRegistrator
from app.service.market_service import MarketService
from app.service.wallet_service import WalletService


class Container(BullflagAbstractFlaskContainer):
    config = BullflagAbstractFlaskContainer.config

    redis_url = providers.Singleton(
        get_redis_url,
        config.app.redis_host,
        config.app.redis_port,
        config.app.redis_user,
        config.app.redis_pass
    )

    mq_url = providers.Singleton(
        get_mq_url,
        config.app.mq_host,
        config.app.mq_port,
        config.app.mq_user,
        config.app.mq_pass
    )

    _celery = providers.Singleton(
        make_celery,
        config.app.name,
        redis_url,
        config.app.redis_mq_backend_db,
        mq_url,
        task_queues=providers.List(
            providers.Object(TOKEN_QUEUE),
            providers.Object(TROLLBOX_QUEUE),
            providers.Object(MARKET_QUEUE),
            providers.Object(WALLET_QUEUE)
        )
    )

    _redis_health_check = providers.Singleton(
        Redis.from_url,
        redis_url,
        config.app.redis_healthcheck_db
    )

    redis_interface_health_check_db = providers.Singleton(
        RedisInterface,
        _redis_health_check
    )

    app = providers.Singleton(
        FlaskApplication,
        config.app
    )

    rest_api = providers.Singleton(
        Api,
        app
    )

    market_celery_producer = providers.Singleton(
        MarketCeleryProducer,
        _celery,
        providers.Object(MARKET_QUEUE)

    )

    _redis_token_db = providers.Singleton(
        Redis.from_url,
        redis_url,
        config.app.redis_token_db
    )

    redis_interface_token_db = providers.Singleton(
        RedisInterface,
        _redis_token_db
    )

    token_celery_producer = providers.Singleton(
        TokenCeleryProducer,
        _celery,
        providers.Object(TOKEN_QUEUE_NAME),
        config.app.token_valid_seconds
    )

    token_service = providers.Singleton(
        TokenService,
        token_celery_producer,
        redis_interface_token_db,
        config.app.secret_key,
        config.app.key_6,
        config.app.token_valid_seconds
    )

    wallet_celery_producer = providers.Singleton(
        WalletCeleryProducer,
        _celery,
        providers.Object(WALLET_QUEUE)
    )

    wallet_service = providers.Singleton(
        WalletService,
        wallet_celery_producer
    )

    market_service = providers.Singleton(
        MarketService,
        market_celery_producer,
        config.assets
    )

    trollbox_celery_producer = providers.Singleton(
        TrollboxCeleryProducer,
        _celery,
        providers.Object(TROLLBOX_QUEUE)
    )

    routes_registrator = providers.Singleton(
        RoutesRegistrator,
        rest_api,
        redis_interface_health_check_db,
        token_service,
        wallet_service,
        market_service,
        trollbox_celery_producer
    )

    # routes_registrator = providers.Singleton(
    #    RoutesRegistrator,
    #    redis_health_check
    # )
#    secrets_provider = providers.Singleton(
#        SecretsProvider
#    )
#
#    block_chain_client_factory = providers.Singleton(
#        BlockChainClientFactory
#    )
#
#    block_chain_client_provider = providers.Singleton(
#        BlockChainClientProvider,
#        config.coin.clients,
#        secrets_provider,
#        block_chain_client_factory
#    )
#
#    block_chain_client = providers.Singleton(
#        BlockChainClient,
#        config.coin.min_confirmations,
#        config.coin.rpc_config_file,
#        secrets_provider
#    )
#
#    withdrawal_service = providers.Singleton(
#        WithdrawalService,
#        block_chain_client
#    )
#
#    utxo_service = providers.Singleton(
#        UtxoService,
#        block_chain_client_provider
#    )
#
#    address_service = providers.Singleton(
#        AddressService,
#        block_chain_client
#    )
#
#    transaction_service = providers.Singleton(
#        TransactionService,
#        block_chain_client
#    )
#
#    mongo_client = providers.Singleton(
#        MongoClient,
#        config.app.mongo_url,
#        username=config.app.mongo_user,
#        password=config.app.mongo_pass,
#        maxPoolSize=50,
#        waitQueueMultiple=10,
#        connect=False
#    )
#

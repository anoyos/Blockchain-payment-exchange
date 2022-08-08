from bullflag_commons.api.v1.internal.redis_healthcheck import RedisHealthCheck
from bullflag_commons.crypto import TokenService
from bullflag_commons.redisinterface import RedisInterface
from bullflag_connector_dummies.v2.trollbox import TrollboxCeleryProducer
from flask_restful import Api

from app.api.v1.market.admin_add_market_v1_resource import AdminAddMarketV1Resource
from app.api.v1.market.admin_update_market_v1_resource import AdminUpdateMarketV1Resource
from app.api.v1.trollbox.admin_add_room_v1_resource import AdminAddTrollboxRoomV1Resource
from app.api.v1.wallet.admin_add_wallet_v1_resource import AdminAddWalletV1Resource
from app.api.v1.wallet.admin_update_wallet_v1_resource import AdminUpdateWalletV1Resource
from app.service.market_service import MarketService
from app.service.wallet_service import WalletService


class RoutesRegistrator:

    def __init__(self,
                 api: Api,
                 redis_interface_health_check: RedisInterface,
                 token_service: TokenService,
                 wallet_service: WalletService,
                 market_service: MarketService,
                 trollbox_celery_producer: TrollboxCeleryProducer):
        self._api = api
        self._redis_interface_health_check = redis_interface_health_check
        self._token_service = token_service
        self._wallet_service = wallet_service
        self._market_service = market_service
        self._trollbox_celery_producer = trollbox_celery_producer
        self.register_routes()

    def register_routes(self):
        self._api.add_resource(
            RedisHealthCheck,
            "/api/v1/a/market/internal/health/",
            endpoint="common_api_v1_internal_health_check",
            resource_class_kwargs={'redis_interface': self._redis_interface_health_check}
        )

        self._api.add_resource(
            AdminAddMarketV1Resource,
            "/api/v1/a/market/add/",
            endpoint="api_v1_admin_market_add",
            resource_class_kwargs={
                'token_service': self._token_service,
                'market_service': self._market_service
            }
        )
        self._api.add_resource(
            AdminUpdateWalletV1Resource,
            "/api/v1/a/wallet/set/",
            endpoint="api_v1_admin_currency_set_currencyid",
            resource_class_kwargs={
                'token_service': self._token_service,
                'wallet_service': self._wallet_service
            }
        )

        self._api.add_resource(
            AdminUpdateMarketV1Resource,
            "/api/v1/a/market/set/",
            endpoint="api_v1_admin_market_set",
            resource_class_kwargs={
                'token_service': self._token_service,
                'market_service': self._market_service
            }
        )

        self._api.add_resource(
            AdminAddTrollboxRoomV1Resource,
            "/api/v1/a/trollbox/rooms/",
            endpoint="api_v1_add_trollbox_room",
            resource_class_kwargs={
                'token_service': self._token_service,
                'trollbox_celery_producer': self._trollbox_celery_producer
            }
        )

        # # Currency
        # self._api.add_resource(
        #     api_v1_admin_currency_profile,
        #     "/api/v1/a/currency/profile/",
        #     endpoint="api_v1_admin_currency_profile",
        # )
        #
        #
        # # Set a wallet setting in the database.
        # self._api.add_resource(
        #     api_v1_admin_currency_set_currencyid,
        #     "/api/v1/a/currency/set/<currencyid>/",
        #     endpoint="api_v1_admin_currency_set_currencyid",
        # )
        #
        #
        # # Market

        #
        # self._api.add_resource(
        #     api_v1_admin_market_set,
        #     "/api/v1/a/market/<settings>/<enable>/",
        #     endpoint="api_v1_admin_market_set_depricated",
        # )
        #

        #
        # self._api.add_resource(
        #     api_v1_admin_market_list,
        #     "/api/v1/a/market/list/",
        #     endpoint="api_v1_admin_market_list",
        # )
        #
        # self._api.add_resource(
        #     api_v1_admin_market_list,
        #     "/api/v1/a/market/list/<basecurrencyid>/",
        #     endpoint="api_v1_admin_market_list_currency",
        # )
        #
        #
        # # User
        # self._api.add_resource(
        #     api_v1_admin_user_profile,
        #     "/api/v1/a/user/profile/",
        #     endpoint="api_v1_admin_user_profile",
        # )
        # self._api.add_resource(
        #     api_v1_admin_user_search,
        #     "/api/v1/a/user/search/",
        #     endpoint="api_v1_admin_user_search",
        # )
        # self._api.add_resource(
        #     api_v1_admin_user_count,
        #     "/api/v1/a/user/count/",
        #     endpoint="api_v1_admin_user_count",
        # )
        #
        # self._api.add_resource(
        #     api_v1_admin_user_list,
        #     "/api/v1/a/user/list/",
        #     endpoint="api_v1_admin_user_list",
        # )

# Not made yet
# self._api.add_resource(api_v1_admin_currency_add, '/api/v1/a/user/edit/')
# self._api.add_resource(api_v1_admin_currency_add, '/api/v1/a/user/set/
# verification/level/')
# self._api.add_resource(api_v1_admin_currency_add, '/api/v1/a/user/verify/
# document/')
# self._api.add_resource(api_v1_admin_currency_add, '/api/v1/a/user/balances/')
# self._api.add_resource(api_v1_admin_currency_add, '/api/v1/a/user/settings/
# password/')
# self._api.add_resource(api_v1_admin_currency_add, '/api/v1/a/user/settings/pin/')
# self._api.add_resource(api_v1_admin_currency_add, '/api/v1/a/user/settings/mfa/')
# self._api.add_resource(api_v1_admin_currency_add, '/api/v1/a/user/settings/
# locked/')
# self._api.add_resource(api_v1_admin_currency_add, '/api/v1/a/user/settings/
# withdrawal/')
# self._api.add_resource(api_v1_admin_currency_add, '/api/v1/a/user/settings/
# admin/')

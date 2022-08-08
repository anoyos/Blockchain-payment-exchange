from typing import Union, Dict

from bitcoinlib import networks
from bitcoinlib.db import get_new_session, init_db
from bitcoinlib.wallets import Wallet, wallets_list
from api_contrib.core.utils import logger


from app import crud, schemas
from app.core.config import settings


def get_network_by_name(asset_code: str, return_description=False) -> Union[str, Dict, None]:
    """ Find coin providers in bitcoinlib network configuration """
    for network_name, network_description in networks.NETWORK_DEFINITIONS.items():
        if network_description['currency_code'] == asset_code:
            if return_description:
                return network_description
            return network_name
    return None


def prepare_database() -> None:
    """ Create tables and wallets in bitcoinlib DB """

    # Create bitcoinlib tables if they doesn't exists
    init_db()

    # Start new SQLAlchemy session
    db_session = get_new_session()

    # get all wallets from database
    wallets_in_db = [w['name'] for w in wallets_list(session=db_session)]

    # For every asset in bullflag platform
    for asset_code in settings.ASSETS:
        # try to find providers for coin
        network = get_network_by_name(asset_code)

        # if coin wallet not and DB and 3rd party provider exists for this coin
        if asset_code not in wallets_in_db and network:
            # TODO: error when execute on empty db
            Wallet.create(asset_code, network=network)

    db_session.close()


def create_eth_system_account():
    """ Create account to accumulate user deposits """
    from app.models.blockchain import SystemAccount
    from app.blockchain.handlers.ethereum.eth import EthCoinHandler

    from os import getenv
    eth_code = getenv('ETH_CURRENCY_CODE', 'tETH')
    system_account = crud.system_account.find_one_sync(query={
        'asset_code': eth_code
    })
    if not system_account:

        handler = EthCoinHandler(asset_code=eth_code)
        new_address = handler.get_new_address()
        assert new_address
        crud.system_account.insert_one_sync(SystemAccount(
            asset_code=eth_code,
            address=new_address
        ))


def create_assets() -> None:
    """
    For every item in assets.json
    Create record in `assets` collection if it doesn't exist
    """
    for currency_code, currency_config in settings.ASSETS.items():

        asset = crud.asset.find_one_sync({"short_name": currency_code})
        created = 0
        if asset:
            logger.info(f"{currency_code} already exists. Update config")
            crud.asset.update_sync(asset, currency_config)
        else:
            crud.asset.insert_one_sync(schemas.Asset(**currency_config))
            logger.info(f"{currency_code} was saved in database")
            # crud.asset.find_one_sync({"_id": row.inserted_id})
            created += 1

        logger.info(f"Total coins in config {len(settings.ASSETS)}. Created: {created}")

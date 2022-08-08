from app.db.init_db import prepare_database, create_eth_system_account, create_assets
from api_contrib.core.utils import logger
from app.stat import fees


def main() -> None:
    logger.info("Creating coin assets")
    create_assets()
    logger.info("Creating initial data")
    prepare_database()
    logger.info("Create system accounts")
    create_eth_system_account()
    logger.info("Update withdrawal fees")
    fees.update_withdrawal_fee()


if __name__ == "__main__":
    create_assets()

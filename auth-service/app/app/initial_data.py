from app.db.init_db import init_db
from api_contrib.core.utils import logger


def main() -> None:
    logger.info("Creating initial data")
    init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()

from api_contrib.core.config import Settings
from pathlib import Path
from os import getenv


class AppSettings(Settings):
    EMAIL_TEMPLATES_DIR: Path = Path(Path(__file__).parent.parent, "email-templates")
    PROJECT_NAME: str = getenv('PROJECT_NAME', 'auth-service')
    API_V1_STR: str = getenv('API_V1_STR', '/api/v1/user')
    TWILIO_ACCOUNT_SID: str = getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN: str = getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_SYSTEM_PHONE: str = getenv('TWILIO_SYSTEM_PHONE', '+19543290413')
    REFRESH_TOKEN_EXPIRE_MINUTES: int = getenv('REFRESH_TOKEN_EXPIRE_MINUTES')


settings = AppSettings()

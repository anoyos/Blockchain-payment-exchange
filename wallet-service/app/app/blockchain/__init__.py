from api_contrib.core import http
from app.core.config import settings


market_service = http.ClientHttp(url=settings.MARKET_SERVICE_URL)
auth_service = http.ClientHttp(url=settings.AUTH_SERVICE_URL)
balance_service = http.ClientHttp(url=settings.BALANCE_SERVICE_URL)

from fastapi import APIRouter

from app.api.api_v1.endpoints import favorites, markets, orderbook, orders, tickers, admin

api_router = APIRouter()
api_router.include_router(admin.router, tags=["admin"], prefix='/admin')
api_router.include_router(favorites.router, tags=["favorites"])
api_router.include_router(markets.router, tags=["markets"])
api_router.include_router(orderbook.router, tags=["orderbook"])
api_router.include_router(orders.router, tags=["orders"])
api_router.include_router(tickers.router, tags=["tickers"])


@api_router.get("/health")
def health_check():
    return {"status": "ok"}

from fastapi import APIRouter

from app.api.api_v1.endpoints import root, balances, wallet, internal, stat, public_traders

api_router = APIRouter()
api_router.include_router(root.router)
api_router.include_router(balances.router)
api_router.include_router(stat.router)
api_router.include_router(wallet.router, prefix='/wallet')
api_router.include_router(internal.router, prefix='/internal')
api_router.include_router(public_traders.router, prefix='/traders')


@api_router.get("/health")
def health_check():
    """ Route for Kubernetes Liveness probe and other monitoring system"""
    return {"status": "ok"}

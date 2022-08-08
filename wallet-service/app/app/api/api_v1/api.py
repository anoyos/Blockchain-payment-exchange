from fastapi import APIRouter

from app.api.api_v1.endpoints import profile, wallet, root, withdrawal, assets

api_router = APIRouter()
api_router.include_router(profile.router, tags=["profile"], prefix='/profile')
api_router.include_router(wallet.router, tags=["wallet"], prefix='/wallet')
api_router.include_router(withdrawal.router, tags=["withdrawal"], prefix='/withdraw')
api_router.include_router(assets.router, tags=["assets"])
api_router.include_router(root.router)


@api_router.get("/health")
def health_check():
    return {"status": "ok"}

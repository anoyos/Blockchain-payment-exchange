from fastapi import APIRouter

from app.api.api_v1.endpoints import (onboarding,
                                      root,
                                      profile,
                                      password,
                                      session,
                                      mfa,
                                      kyc,
                                      admin,
                                      api_keys)

api_router = APIRouter()
api_router.include_router(root.router, tags=["user"])
api_router.include_router(session.router, tags=["session"], prefix='/session')
api_router.include_router(admin.router, tags=["admin"], prefix='/admin')
api_router.include_router(onboarding.router, tags=["user"], prefix='/onboarding')
api_router.include_router(password.router, tags=["password"], prefix='/reset')
api_router.include_router(profile.router, tags=["user"], prefix='/profile')
api_router.include_router(kyc.router, tags=["kyc"], prefix='/profile')
api_router.include_router(mfa.router, tags=["mfa"], prefix='/mfa')
api_router.include_router(api_keys.router, tags=["api_keys"], prefix='/apikey')


@api_router.get("/health")
def health_check():
    return {"status": "ok"}

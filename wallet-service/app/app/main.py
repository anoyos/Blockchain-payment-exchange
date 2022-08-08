from api_contrib.core.errors import base_error_handler
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.engine import client, client_sync

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"{settings.API_V1_STR}/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("shutdown", client.close)
app.add_event_handler("shutdown", client_sync.close)

app.add_exception_handler(HTTPException, base_error_handler)

app.include_router(api_router, prefix=settings.API_V1_STR)

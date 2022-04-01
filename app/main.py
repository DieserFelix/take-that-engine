from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import app.routers as routers
from app.lib.environment import CREATE_DATABASE, CORS_ORIGINS

if CREATE_DATABASE:
    pass

app = FastAPI()
origins = CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers.routers:
    app.include_router(router)

app.openapi_schema = get_openapi(
    title="Take That Engine",
    version="0.1",
    description="Take That is a card game.",
    routes=app.routes
)
from asyncio.log import logger
from uuid import uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.lib import create_access_token
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

@app.get("/api")
def ident():
    print("Assigning new UUID")
    return create_access_token(dict(sub=str(uuid4())))

for router in routers.routers:
    app.include_router(router)
    

app.openapi_schema = get_openapi(
    title="Take That Engine",
    version="0.1",
    description="Take That is a card game.",
    routes=app.routes
)
import asyncio
import io
import threading
from contextlib import asynccontextmanager

import avro.schema
from avro.io import DatumReader, BinaryDecoder
from fastapi import FastAPI, WebSocket
from kafka import KafkaConsumer
from starlette import status

from src.settings.config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    DOCS_URL,
)
from src.settings.database import sessionmanager
from src.settings.websockets import ConnectionManager
from src.user.router import router as router_user
from src.notification.router import router as router_notification
from src.channel.router import router as router_channel


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    """
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan,
    description=APP_DESCRIPTION,
    docs_url=DOCS_URL,
    redoc_url=None,
    swagger_ui_parameters={
        "docExpansion": "none"
    },
    title=APP_NAME,
    version=APP_VERSION,
)

app.include_router(router_user, prefix="/user", tags=["User"])
app.include_router(router_notification, prefix="/notification", tags=["Notification"])
app.include_router(router_channel, prefix="/channel", tags=["Channel"])


@app.get(path="/root", status_code=status.HTTP_200_OK)
def root():
    return {"Connected to Cintelink Notifications"}

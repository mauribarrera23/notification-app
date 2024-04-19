import asyncio
import io
import threading
from contextlib import asynccontextmanager

import avro.schema
from avro.io import DatumReader, BinaryDecoder
from fastapi import FastAPI, WebSocket, Depends
from kafka import KafkaConsumer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.settings.config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    DOCS_URL,
    KAFKA_HOST,
    KAFKA_PORT,
)
from src.settings.database import sessionmanager, get_db_session
from src.settings.websockets import ConnectionManager
from src.user.dependencies import get_websocket_current_user
from src.user.models import User
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
    openapi_prefix="/api/v1"
)

app.include_router(router_user, prefix="/user", tags=["User"])
app.include_router(router_notification, prefix="/notification", tags=["Notification"])
app.include_router(router_channel, prefix="/channel", tags=["Channel"])

manager = ConnectionManager()

consumer = KafkaConsumer(
    "postgres.public.notification",
    bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"],
)

websocket_connections = []


async def kafka_listener():
    schema = avro.schema.parse("""
            {
                "type": "record",
                "name": "notification",
                "fields": [
                    {
                        "name": "id",
                        "type": "string",
                        "default": false
                    }
                ]
            }
        """)
    for message in consumer:
        reader = DatumReader(schema)
        message_bytes = io.BytesIO(message.value)
        message_bytes.seek(7)
        decoder = BinaryDecoder(message_bytes)
        event_dict = reader.read(decoder)
        for ws in websocket_connections:
            await ws.send_text(event_dict.get("id", None))


@app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket, _: User = Depends(get_websocket_current_user)):
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket=websocket)
    websocket_connections.append(websocket)
    try:
        while websocket in websocket_connections:
            mensaje = await websocket.receive_text()
            await manager.broadcast_message(mensaje)
    except Exception as e:
        print(f"Websocket error connection: {e}")
    finally:
        manager.disconnect(websocket=websocket)
        websocket_connections.remove(websocket)


@app.get(path="/root", status_code=status.HTTP_200_OK)
def root():
    return {"Connected to Cintelink Notifications"}


def start_kafka_listener():
    asyncio.run(kafka_listener())


kafka_thread = threading.Thread(target=start_kafka_listener)
kafka_thread.start()

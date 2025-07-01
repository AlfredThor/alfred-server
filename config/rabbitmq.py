import asyncio
from settings.env import RABBITMQ_URL
from aio_pika import connect_robust, RobustConnection

_connection: RobustConnection | None = None

async def get_rabbitmq_connection() -> RobustConnection:
    global _connection
    if _connection is None or _connection.is_closed:
        _connection = await connect_robust(RABBITMQ_URL)
    return _connection

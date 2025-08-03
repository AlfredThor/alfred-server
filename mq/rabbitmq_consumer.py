from aio_pika import connect_robust, IncomingMessage
from config.rabbitmq import RABBITMQ_URL


class RabbitMQConsumer:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        self.connection = await connect_robust(RABBITMQ_URL)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)

    async def consume(self, callback):
        await self.connect()
        await self.queue.consume(self._wrap_callback(callback))
        print(f"[*] Waiting for messages in {self.queue_name}...")

    def _wrap_callback(self, callback):
        async def wrapper(message: IncomingMessage):
            async with message.process():
                await callback(message.body.decode())
        return wrapper

    async def close(self):
        await self.channel.close()
        await self.connection.close()


# 示例调用
if __name__ == '__main__':
    # consumer_demo.py
    import asyncio

    async def handle_message(body: str):
        print("Received:", body)


    async def main():
        consumer = RabbitMQConsumer("my_queue")
        await consumer.consume(handle_message)
        await asyncio.Future()  # keep running


    asyncio.run(main())

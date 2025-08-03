from aio_pika import connect_robust, Message
from config.rabbitmq import RABBITMQ_URL


class RabbitMQProducer:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = await connect_robust(RABBITMQ_URL)
            self.channel = await self.connection.channel()

    async def send(self, queue_name: str, message_body: str):
        await self.connect()
        await self.channel.declare_queue(queue_name, durable=True)
        await self.channel.default_exchange.publish(
            Message(body=message_body.encode()),
            routing_key=queue_name,
        )

    async def close(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()


if __name__ == '__main__':
    # producer_demo.py
    import asyncio

    async def main():
        producer = RabbitMQProducer()
        await producer.send("my_queue", "Hello from class-based producer!")
        await producer.close()


    asyncio.run(main())

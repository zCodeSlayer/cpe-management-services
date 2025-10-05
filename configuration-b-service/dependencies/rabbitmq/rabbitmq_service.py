import asyncio
import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractChannel
from aio_pika.exceptions import QueueEmpty

__all__ = ["RabbitMQService"]


class RabbitMQService:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        login: str = "guest",
        password: str = "guest",
    ):
        self.__host: str = host
        self.__port: int = port
        self.__login: str = login
        self.__password: str = password

        self.__connection: AbstractRobustConnection | None = None
        self.__channel: AbstractChannel | None = None

    async def __aenter__(self) -> "RabbitMQService":
        self.__connection = await aio_pika.connect_robust(
            login=self.__login,
            password=self.__password,
            host=self.__host,
            port=self.__port,
        )
        self.__channel = await self.__connection.channel()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.__channel and not self.__channel.is_closed:
                await self.__channel.close()
        finally:
            if self.__connection and not self.__connection.is_closed:
                await self.__connection.close()

    async def get_message(self, queue_name: str) -> str | None:
        queue: aio_pika.abc.AbstractQueue = await self.__channel.declare_queue(
            queue_name, durable=True, auto_delete=False
        )
        try:
            incoming = await queue.get(no_ack=True)
        except QueueEmpty as e:
            return None

        if incoming is None:
            return None

        return incoming.body.decode("utf-8")

    async def send_message(self, queue_name: str, message: str) -> None:
        body: bytes = message.encode("utf-8")
        msg = aio_pika.Message(
            body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            content_type="text/plain; charset=utf-8",
        )
        await self.__channel.default_exchange.publish(msg, routing_key=queue_name)

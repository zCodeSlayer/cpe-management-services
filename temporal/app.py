import asyncio
import aiohttp

from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from schemas.rabbitmq_message_schemas import ConfigurationMessageSchema
from config import Settings

settings = Settings()

broker = RabbitBroker(
    f"amqp://{settings.rabbitmq_login}:{settings.rabbitmq_password}@{settings.rabbitmq_host}:{settings.rabbitmq_port}/"
)
app = FastStream(broker)


@broker.subscriber(RabbitQueue("externally_configured_queue_1", durable=True))
@broker.publisher(RabbitQueue("externally_configured_queue_2", durable=True))
async def redirect_configuration_massage(
    configuration_massage: ConfigurationMessageSchema,
) -> ConfigurationMessageSchema:
    print("Received configuration massage:", configuration_massage)
    configuration_data = configuration_massage.configuration.model_dump(by_alias=True)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.configuration_a_service_url}/api/v1/equipment/cpe/{configuration_massage.equipment_id}",
            json=configuration_data,
        ) as resp:
            print(resp.status)
            print(await resp.text())

    return configuration_massage


async def main():
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())

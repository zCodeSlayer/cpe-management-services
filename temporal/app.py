import asyncio
import aiohttp

from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from schemas.rabbitmq_message_schemas import ConfigurationMessageSchema


broker = RabbitBroker("amqp://guest:guest@localhost:5672/")

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
            f"http://127.0.0.1:8000/api/v1/equipment/cpe/{configuration_massage.equipment_id}",
            json=configuration_data,
        ) as resp:
            print(resp.status)
            print(await resp.text())

    return configuration_massage


async def main():
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())

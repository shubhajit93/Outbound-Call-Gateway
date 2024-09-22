import asyncio
from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig
from nats_publisher.config.config import NATS_URL, STREAM_NAME, BASE_SUBJECT


class StreamManager:
    def __init__(self, nats_url, stream_name, base_subject):
        self.nats_url = nats_url
        self.stream_name = stream_name
        self.base_subject = base_subject

    async def create_stream(self):
        nc = NATS()
        await nc.connect(servers=[self.nats_url])
        js = nc.jetstream()

        config = StreamConfig(
            name=self.stream_name,
            subjects=[f"{self.base_subject}.*.*"],
            retention="workqueue",
            storage="file",
            discard="old",
            num_replicas=1
        )
        await js.add_stream(config=config)
        print(f"Stream {self.stream_name} created successfully.")
        await nc.close()


async def run_create_stream():
    manager = StreamManager(NATS_URL, STREAM_NAME, BASE_SUBJECT)
    await manager.create_stream()


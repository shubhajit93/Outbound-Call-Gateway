import asyncio
from nats.aio.client import Client as NATS
from nats.js.api import ConsumerConfig
from nats_consumer.config.config import NATS_URL, STREAM_NAME, BASE_SUBJECT, CONSUMER_WORKER_COUNT, BATCH_SIZE


class Consumer:
    def __init__(self, consumer_name):
        self.nats_url = NATS_URL
        self.stream_name = STREAM_NAME
        self.consumer_name = consumer_name
        self.subject_filter = f"{BASE_SUBJECT}.{consumer_name}.*"
        self.batch_size = BATCH_SIZE
        self.worker_count = CONSUMER_WORKER_COUNT
        self.nc = None
        self.js = None

    async def connect(self):
        self.nc = NATS()
        await self.nc.connect(servers=[self.nats_url])
        self.js = self.nc.jetstream()
        print("Consumer is connected to NATS server")

    async def create_consumer(self):
        config = ConsumerConfig(
            durable_name=self.consumer_name,
            ack_policy="explicit",
            max_deliver=1,
            filter_subject=self.subject_filter,
            deliver_policy="all",
            replay_policy="instant",
            max_ack_pending=10000
        )

        await self.js.add_consumer(stream=self.stream_name, config=config)
        print(
            f"Consumer '{self.consumer_name}' added to stream '{self.stream_name}' with filter '{self.subject_filter}'")

    async def close(self):
        await self.nc.close()
        print("NATS is Disconnected")

    async def worker(self, worker_id):
        sub = await self.js.pull_subscribe(
            self.subject_filter,
            durable=self.consumer_name,
            stream=self.stream_name
        )
        print(f"Worker {worker_id} started.")

        while True:
            try:
                msgs = await sub.fetch(self.batch_size, timeout=5)
                for msg in msgs:
                    print(f"worker_id: {worker_id} receives message: {msg.data.decode()}")
                    await msg.ack()

            except asyncio.TimeoutError:
                print(f"Worker {worker_id}: No messages available, waiting...")

            except Exception as e:
                await self.close()
                print(f"Worker {worker_id} error: {e}")
                break

    async def run_worker(self):
        tasks = []
        for i in range(self.worker_count):
            task = asyncio.create_task(self.worker(i + 1))
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def run(self):
        await self.connect()
        await self.create_consumer()
        await self.run_worker()


async def run_consumer(consumer_name):
    consumer = Consumer(
        consumer_name
    )
    await consumer.run()


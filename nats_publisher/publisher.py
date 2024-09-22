import random
from nats.aio.client import Client as NATS


class Publisher:
    def __init__(self, nats_url, base_subject, service_mapping):
        self.nats_url = nats_url
        self.base_subject = base_subject
        self.service_mapping = service_mapping

    async def publish_message(self, service_name, data):
        nc = NATS()
        await nc.connect(servers=[self.nats_url])

        js = nc.jetstream()

        if service_name in self.service_mapping:
            asterisk = random.choice(self.service_mapping[service_name])
            subject = f"{self.base_subject}.{asterisk}.{service_name}"
            ack = await js.publish(subject, data.encode())
            print(f"Published message to {subject} with sequence: {ack.seq}")

        else:
            print(f"Service name '{service_name}' not found in mapping configuration.")

        await nc.close()

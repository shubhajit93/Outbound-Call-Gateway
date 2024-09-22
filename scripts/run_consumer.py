import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nats_consumer.consumer import run_consumer


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_consumer.py <consumer-name>")
        sys.exit(1)

    consumerName = sys.argv[1]
    asyncio.run(run_consumer(consumerName))

import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nats_publisher.stream_manager.stream_manager import run_create_stream

if __name__ == "__main__":
    asyncio.run(run_create_stream())

import os
from dotenv import load_dotenv

load_dotenv()

NATS_URL = os.getenv("NATS_URL")
STREAM_NAME = os.getenv("STREAM_NAME")
BASE_SUBJECT = os.getenv("BASE_SUBJECT")
BATCH_SIZE = int(os.getenv("BATCH_SIZE"))
CONSUMER_WORKER_COUNT = int(os.getenv("CONSUMER_WORKER_COUNT"))


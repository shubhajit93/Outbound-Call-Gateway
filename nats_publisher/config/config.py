import os
from dotenv import load_dotenv

load_dotenv()

NATS_URL = os.getenv("NATS_URL")
STREAM_NAME = os.getenv("STREAM_NAME")
BASE_SUBJECT = os.getenv("BASE_SUBJECT")
PORT = int(os.getenv("PORT"))

SERVICE_MAPPING = {
    "psb": ["consumer-1", "consumer-3"],
    "uddipan": ["consumer-2", "consumer-3"],
    "sajida": ["consumer-1", "consumer-2"]
}

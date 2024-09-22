import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nats_publisher.webhook_listener import run_webhook_listener

if __name__ == "__main__":
    run_webhook_listener()

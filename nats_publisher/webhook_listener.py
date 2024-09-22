from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from nats_publisher.publisher import Publisher
from nats_publisher.config.config import NATS_URL, PORT, BASE_SUBJECT, SERVICE_MAPPING
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrganizationInfo(BaseModel):
    organizationId: Optional[str]
    organizationName: Optional[str]
    hoId: Optional[str]
    hoName: Optional[str]
    zoneId: Optional[str]
    zoneName: Optional[str]
    areaId: Optional[str]
    areaName: Optional[str]
    branchId: Optional[str]
    branchName: Optional[str]
    centerId: Optional[str]
    centerName: Optional[str]
    services: Optional[List] = None
    merchantWallets: Optional[Dict] = None


class CustomerInfo(BaseModel):
    customerType: Optional[str]
    customerId: Optional[str]
    customerName: Optional[str]
    organization: Optional[OrganizationInfo] = None


class Body(BaseModel):
    phoneNumber: Optional[str]
    customerInfo: Optional[List[CustomerInfo]] = None
    customerTypeServices: Optional[Dict] = None
    customerWallets: Optional[Dict] = None


class UserIdentity(BaseModel):
    body: Optional[Body] = None


class Call(BaseModel):
    bno: Optional[str]
    correlationId: Optional[str]
    serviceType: Optional[str]
    content: Optional[str]
    instantPay: Optional[bool]
    userIdentity: Optional[UserIdentity] = None


class WebhookRequest(BaseModel):
    organization: str
    calls: Optional[List[Call]] = None


class WebhookListener:
    def __init__(self, port, publisher):
        self.port = port
        self.publisher = publisher
        self.app = FastAPI()

        @self.app.post("/outbounds/gateway/webhook")
        async def webhook(request: Request):
            try:
                webhook_data = WebhookRequest.parse_obj(await request.json())
                organization = webhook_data.organization
                calls = webhook_data.calls

                if not organization or not calls:
                    logger.error("Invalid request data: missing organization or calls")
                    raise HTTPException(status_code=400, detail="Invalid request: missing organization or calls")

                logger.info(f"organization: {organization} with {len(calls)} calls")

                for call in calls:
                    message_dict = call.dict()
                    message_dict['organization'] = organization
                    # Converts input dictionary into string and stores it in json_string
                    logger.info(f"Publishing message: {json.dumps(message_dict, ensure_ascii=False)}")
                    await self.publisher.publish_message(organization, json.dumps(message_dict, ensure_ascii=False))

                return {"status": "success", "message": "Messages published successfully"}

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)


def run_webhook_listener():
    publisher = Publisher(NATS_URL, BASE_SUBJECT, SERVICE_MAPPING)
    listener = WebhookListener(PORT, publisher)
    listener.run()

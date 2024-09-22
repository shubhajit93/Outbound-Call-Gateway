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
                json_data = await request.json()
                organization = json_data.get('organization')
                calls = json_data.get('calls')

                logger.info(f"Received webhook for organization: {organization} with {len(calls)} calls")

                if not organization or not calls:
                    logger.error("Invalid request data: missing organization or calls")
                    raise HTTPException(status_code=400, detail="Invalid request: missing organization or calls")

                for call in calls:
                    message_dict = call.dict()
                    message_dict['organization'] = organization
                    print(message_dict)
                    await self.publisher.publish_message(organization, "Hello")

                return {"status": "success", "message": "Message published successfully"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            # print(calls)
            # print(f"service name: {service_name}")
            #
            # # print(f"Organization: {service_name}")
            # # print(f"Content: {content}")
            # await self.publisher.publish_message(service_name, "Hello")

            # if service_name:
            #     message = str(content)
            #     await self.publisher.publish_message(service_name, message)
            #     return {"status": "success", "service_name": service_name, "message": "ok"}
            # else:
            #     return {"status": "error", "message": "serviceName not provided"}

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)


def run_webhook_listener():
    publisher = Publisher(NATS_URL, BASE_SUBJECT, SERVICE_MAPPING)
    listener = WebhookListener(PORT, publisher)
    listener.run()

from fastapi import APIRouter, Query, status
from fastapi.responses import PlainTextResponse
from models.webhook_model import WebhookData
from core.config import VERIFY_TOKEN

router = APIRouter()

@router.post("/webhooks")
async def facebook_webhook(data: WebhookData):
    print("Received webhook:", data.dict())
    return {"status": "received"}

@router.get("/webhooks")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: int = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=str(hub_challenge), status_code=status.HTTP_200_OK)
    return PlainTextResponse(content="Invalid token", status_code=status.HTTP_403_FORBIDDEN)

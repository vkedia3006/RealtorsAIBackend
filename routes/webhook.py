from fastapi import APIRouter, Request, Query, status
from fastapi.responses import PlainTextResponse
from models.webhook_model import WebhookData
from core.config import VERIFY_TOKEN
from facebook.lead_parser import extract_lead_data
from facebook.lead_handler import process_lead_and_create_conversation

public_router = APIRouter()

@public_router.post("/webhooks")
async def facebook_webhook(request: Request):
    body = await request.json()
    print("📩 Raw Facebook webhook payload:", body)

    entries = body.get("entry", [])
    for entry in entries:
        for change in entry.get("changes", []):
            value = change.get("value", {})
            ad_id = value.get("ad_id")
            lead_id = value.get("id")

            if not ad_id or not lead_id:
                continue

            lead_data = extract_lead_data(value)
            if lead_data:
                await process_lead_and_create_conversation(ad_id, lead_id, lead_data)

    return {"status": "received"}

@public_router.get("/webhooks")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: int = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=str(hub_challenge), status_code=status.HTTP_200_OK)
    return PlainTextResponse(content="Invalid token", status_code=status.HTTP_403_FORBIDDEN)

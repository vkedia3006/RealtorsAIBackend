from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime, UTC
from bson import ObjectId
from twilio_client.sender import send_sms

from core.database import collections, with_meta
from llm.generator import generate_message

public_router = APIRouter()

@public_router.post("/sms")
async def incoming_sms(request: Request):
    form = await request.form()
    incoming_text = form.get("Body", "").strip()
    from_number = form.get("From")

    print(f"📩 Incoming SMS from {from_number}: {incoming_text}")

    # 1. Find existing conversation by phone number
    conversation = await collections.conversations.find_one({"phone": from_number})
    if not conversation:
        raise HTTPException(status_code=400, detail="No matching conversation for phone number")

    conversation_id = conversation["_id"]
    user_name = conversation.get("userName", "there")
    now = datetime.now(UTC)

    # 2. Store incoming message
    await collections.messages.insert_one(with_meta({
        "conversation_id": conversation_id,
        "sender": "user",
        "text": incoming_text
    }))

    # 3. Generate LLM response
    reply_text = await generate_message(str(conversation_id), user_name)

    # 4. Store outgoing message
    await collections.messages.insert_one(with_meta({
        "conversation_id": conversation_id,
        "sender": "agent",
        "text": reply_text
    }))
    
    send_sms(from_number, reply_text)

    return JSONResponse(status_code=200, content={"message": "Message sent successfully"})

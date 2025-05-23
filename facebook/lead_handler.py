from core.database import collections
from llm.generator import generate_message
from twilio_client.sender import send_sms
from datetime import datetime
from bson import ObjectId
from utils.db_meta_data import with_meta

async def process_lead_and_create_conversation(ad_id: str, lead_id: str, lead: dict):
    now = datetime.utcnow()

    # 1. Create conversation
    convo_doc = with_meta({
        "ad_id": ObjectId(ad_id),
        "userName": lead["name"],
        "phone": lead["phone"],
        "email": lead["email"],
        "userImage": "https://placekitten.com/40/40",
        "lastActive": now,
        "unread": True,
        "lead_id": lead_id
    })
    convo_result = await collections.conversations.insert_one(convo_doc)

    # 2. Generate + send message
    message_text = await generate_message(str(convo_result.inserted_id), lead["name"])
    send_sms(lead["phone"], message_text)

    # 3. Store message
    await collections.messages.insert_one(with_meta({
        "conversation_id": convo_result.inserted_id,
        "sender": "agent",
        "text": message_text
    }))

    return convo_result.inserted_id

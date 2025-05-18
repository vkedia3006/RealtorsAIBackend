from openai import OpenAI
from core.database import collections
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

async def generate_message(lead_id: str, name: str, message: str = "") -> str:
    lead_object_id = ObjectId(lead_id)
    
    # Fetch prior messages
    messages_cursor = collections.messages.find({"conversation_id": lead_object_id}).sort("meta.created_at", 1)
    messages = await messages_cursor.to_list(None)

    chat_messages = [
        {"role": "system", "content": "You are a helpful real estate assistant. Your job is to write SMS replies on behalf of an agent."}
    ]

    # Case 1: New conversation — send welcome
    if not messages:
        chat_messages += [
            {"role": "user", "content": f"A new lead named {name} just filled out a form. Send a warm, professional welcome message via SMS. Keep it short, friendly, and human."}
        ]
    else:
        # Case 2: Ongoing conversation — read all messages
        for msg in messages:
            role = "user" if msg["sender"] == "user" else "assistant"
            chat_messages.append({
                "role": role,
                "content": msg["text"]
            })

        # Prompt for response continuation
        chat_messages.append({
            "role": "user",
            "content": "Craft a thoughtful next reply that continues this conversation."
        })

    try:
        response = client.chat.completions.create(
            model="grok-2-latest",
            messages=chat_messages,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        raise RuntimeError(f"Grok LLM error: {str(e)}")


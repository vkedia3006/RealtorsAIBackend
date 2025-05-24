from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from core.database import collections
from auth.dependencies import get_current_user

protected_router = APIRouter(dependencies=[Depends(get_current_user)])
@protected_router.get("/conversations/{ad_id}")

async def get_conversations_for_ad(ad_id: str, user=Depends(get_current_user)):
    user_id = user["user_id"]

    # 1. Validate and find ad
    ad = await collections.ads.find_one({"_id": ObjectId(ad_id)})
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")

    # 2. Find associated page
    page = await collections.pages.find_one({"_id": ad["page_id"], "user_id": user_id})
    if not page:
        raise HTTPException(status_code=403, detail="Unauthorized access to ad")

    # 3. Fetch all conversations for that ad
    conversations = await collections.conversations.find({"ad_id": ObjectId(ad_id)}).to_list(None)
    conversation_ids = [c["_id"] for c in conversations]

    # 4. Fetch all messages for those conversations
    messages = await collections.messages.find({
        "conversation_id": {"$in": conversation_ids}
    }).to_list(None)

    # 5. Group messages by conversation_id
    message_map = {}
    for msg in messages:
        cid = str(msg["conversation_id"])
        message_map.setdefault(cid, []).append({
            "id": str(msg["_id"]),
            "sender": msg["sender"],
            "text": msg["text"],
            "timestamp": msg["timestamp"]
        })

    # 6. Structure final response
    result = {
        "adId": str(ad["_id"]),
        "adName": ad["name"],
        "pageName": page["name"],
        "conversations": [
            {
                "id": str(c["_id"]),
                "userName": c.get("userName", "Lead"),
                "userImage": c.get("userImage", "https://placekitten.com/40/40"),
                "phone": c.get("userPhone", "+000000"),
                "email": c.get("email", "xyz@xyz.com"),
                "active": True,
                "botActive": True,
                "messages": message_map.get(str(c["_id"]), [])
            }
            for c in conversations
        ]
    }

    return result

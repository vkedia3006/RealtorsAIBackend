from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user
from bson import ObjectId
from core.database import collections

protected_router = APIRouter(dependencies=[Depends(get_current_user)])

@protected_router.get("/dashboard-data")
async def get_dashboard_data(user=Depends(get_current_user)):
    user_id = user["user_id"]

    # 1. Fetch pages for user
    pages = await collections.pages.find({"user_id": user_id}).to_list(None)
    if not pages:
        return {"pages": [], "conversations": []}

    page_ids = [page["_id"] for page in pages]

    # 2. Fetch ads for those pages
    ads = await collections.ads.find({"page_id": {"$in": page_ids}}).to_list(None)
    ad_ids = [ad["_id"] for ad in ads]

    # 3. Fetch conversations for those ads
    conversations = await collections.conversations.find({
        "ad_id": {"$in": ad_ids}
    }).to_list(None)

    conv_ids = [c["_id"] for c in conversations]

    # 4. Fetch last message for each conversation
    messages = await collections.messages.aggregate([
        {"$match": {"conversation_id": {"$in": conv_ids}}},
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$conversation_id",
            "lastMessage": {"$first": "$text"},
            "lastActive": {"$first": "$timestamp"}
        }}
    ]).to_list(None)

    last_message_map = {m["_id"]: m for m in messages}

    # 5. Build flat conversation list (for conversation tab)
    conversation_list = []
    for conv in conversations:
        msg_data = last_message_map.get(conv["_id"], {})
        conversation_list.append({
            "id": str(conv["_id"]),
            "userName": conv.get("userName", "Lead"),
            "userImage": conv.get("userImage", "https://placekitten.com/40/40"),
            "adId": str(conv["ad_id"]),
            "adName": "",  # Will be added below
            "lastMessage": msg_data.get("lastMessage", ""),
            "timestamp": msg_data.get("lastActive"),
            "unread": conv.get("unread", False)
        })

    # 6. Attach adName to each conversation (ad_id → name)
    ad_id_to_name = {str(ad["_id"]): ad["name"] for ad in ads}
    for conv in conversation_list:
        conv["adName"] = ad_id_to_name.get(conv["adId"], "Unknown Ad")

    # 7. Build ad summaries for each page
    ad_map = {}
    for ad in ads:
        ad_id = str(ad["_id"])
        ad_convs = [c for c in conversation_list if c["adId"] == ad_id]
        last_active = max((c["timestamp"] for c in ad_convs if c["timestamp"]), default=None)

        ad_map[ad_id] = {
            "id": ad_id,
            "name": ad["name"],
            "conversations": len(ad_convs),
            "lastActive": last_active,
            "is_deleted": ad.get("isDeleted", False)
        }

    # 8. Build final page list
    result_pages = []
    for page in pages:
        page_ads = [
            ad_map[str(ad["_id"])]
            for ad in ads if ad["page_id"] == page["_id"]
        ]
        result_pages.append({
            "id": str(page["_id"]),
            "name": page["name"],
            "imageUrl": page.get("imageUrl", "https://placekitten.com/64/64"),
            "ads": page_ads,
            "is_deleted": page.get("isDeleted", False)
        })

    return {
        "pages": result_pages,
        "conversations": conversation_list
    }

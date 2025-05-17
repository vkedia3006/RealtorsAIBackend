from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user
from utils.serializers import serialize_doc
from bson import ObjectId
from core.database import collections

protected_router = APIRouter(dependencies=[Depends(get_current_user)])

@protected_router.get("/dashboard-data")
async def get_dashboard_data(user=Depends(get_current_user)):
    user_id = user["user_id"]

    # 1. Fetch pages for user
    pages = await collections.pages.find({ "user_id": user_id }).to_list(None)

    if not pages:
        return { "pages": [] }

    page_ids = [page["_id"] for page in pages]

    # 2. Fetch ads for those pages
    ads = await collections.ads.find({ "page_id": { "$in": page_ids } }).to_list(None)
    ad_ids = [ad["_id"] for ad in ads]

    # 3. Fetch all conversations for those ads
    conversations = await collections.conversations.find({
        "ad_id": { "$in": ad_ids }
    }).to_list(None)

    # 4. Fetch last messages per conversation (optional optimization below)
    conv_map = {}
    for conv in conversations:
        ad_id = str(conv["ad_id"])
        if ad_id not in conv_map:
            conv_map[ad_id] = {
                "count": 0,
                "lastActive": None
            }

        conv_map[ad_id]["count"] += 1
        ts = conv.get("lastActive")
        if ts and (not conv_map[ad_id]["lastActive"] or ts > conv_map[ad_id]["lastActive"]):
            conv_map[ad_id]["lastActive"] = ts
    
    last_message_map = { m["_id"]: m for m in messages }

    # 5. Organize data
    ad_map = {}
    for ad in ads:
        ad_id = str(ad["_id"])
        conv_data = conv_map.get(ad_id, {"count": 0, "lastActive": None})
        ad_map[ad_id] = {
            "id": ad_id,
            "name": ad["name"],
            "conversations": conv_data["count"],
            "lastActive": conv_data["lastActive"],
        }

    result = []
    for page in pages:
        page_ads = [
            ad_map[str(ad["_id"])]
            for ad in ads if ad["page_id"] == page["_id"]
        ]
        result.append({
            "id": str(page["_id"]),
            "name": page["name"],
            "imageUrl": page.get("imageUrl", "https://placekitten.com/64/64"),  # fallback
            "ads": page_ads
        })

    return { "pages": result }

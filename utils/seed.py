import asyncio
from datetime import datetime, timedelta, UTC
from core.database import collections

# User ID
user_id = "7c947dd6-b12b-4ce1-b056-ffa3e8c42a92"

async def seed():
    # 🔥 Delete old data
    await collections.messages.delete_many({})
    await collections.conversations.delete_many({})
    await collections.ads.delete_many({})
    await collections.pages.delete_many({})

    print("🧹 Old data deleted.")

    # 📄 Insert Pages
    pages_data = [
        {"user_id": user_id, "name": "Urban Realty Group", "imageUrl": "https://placekitten.com/64/64"},
        {"user_id": user_id, "name": "Coastal Properties", "imageUrl": "https://placekitten.com/65/65"},
        {"user_id": user_id, "name": "Mountain View Estates", "imageUrl": "https://placekitten.com/66/66"},
        {"user_id": user_id, "name": "Lakeside Realty", "imageUrl": "https://placekitten.com/67/67"},
    ]
    page_ids = [ (await collections.pages.insert_one(p)).inserted_id for p in pages_data ]

    # 🏘 Insert Ads
    ads_data = [
        {"page_id": page_ids[0], "name": "Downtown Lofts"},
        {"page_id": page_ids[0], "name": "Suburban Homes"},
        {"page_id": page_ids[1], "name": "Oceanfront Condos"},
        {"page_id": page_ids[1], "name": "Beach Houses"},
        {"page_id": page_ids[2], "name": "Mountain Cabins"},
        {"page_id": page_ids[2], "name": "Ski Chalets"},
        {"page_id": page_ids[3], "name": "Lakefront Villas"},
        {"page_id": page_ids[3], "name": "Woodland Cottages"},
    ]
    ad_ids = [ (await collections.ads.insert_one(ad)).inserted_id for ad in ads_data ]

    # 💬 Insert Conversations
    conversation_templates = [
        ("John Smith", "https://placekitten.com/40/40", 0, True),
        ("Sarah Johnson", "https://placekitten.com/41/41", 1, False),
        ("Michael Brown", "https://placekitten.com/42/42", 2, True),
        ("Emily Davis", "https://placekitten.com/43/43", 3, True),
        ("Daniel Garcia", "https://placekitten.com/44/44", 4, False),
        ("Laura Wilson", "https://placekitten.com/45/45", 5, True),
        ("James Lee", "https://placekitten.com/46/46", 6, False),
        ("Natalie Young", "https://placekitten.com/47/47", 7, True),
    ]
    conversation_ids = []
    for name, img, i, unread in conversation_templates:
        convo = await collections.conversations.insert_one({
            "ad_id": ad_ids[i],
            "userName": name,
            "userImage": img,
            "lastActive": datetime.now(UTC) - timedelta(hours=i),
            "unread": unread
        })
        conversation_ids.append(convo.inserted_id)

    # 📥 Insert Messages
    message_texts = [
        "I'm interested in scheduling a viewing for this property.",
        "What are the HOA fees for this listing?",
        "Is the property still available?",
        "Can I book a visit for next weekend?",
        "Are pets allowed in this home?",
        "Is there a virtual tour I can view?",
        "How far is this from downtown?",
        "Do these homes come with a garage?"
    ]
    messages = [{
        "conversation_id": conversation_ids[i],
        "sender": "user",
        "text": message_texts[i],
        "timestamp": datetime.now(UTC) - timedelta(hours=i)
    } for i in range(len(conversation_ids))]

    await collections.messages.insert_many(messages)

    print("✅ Dummy data seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed())

=import asyncio
import random
from datetime import datetime, timedelta, UTC
from core.database import collections

# User ID
user_id = "7c947dd6-b12b-4ce1-b056-ffa3e8c42a92"

page_names = [
    "Urban Realty Group", "Coastal Properties", "Mountain View Estates", "Lakeside Realty"
]
ad_names = [
    "Downtown Lofts", "Suburban Homes", "Oceanfront Condos", "Beach Houses",
    "Mountain Cabins", "Ski Chalets", "Lakefront Villas", "Woodland Cottages"
]
user_names = [
    "John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis",
    "Daniel Garcia", "Laura Wilson", "James Lee", "Natalie Young"
]
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

def random_timestamp(offset_days=5):
    now = datetime.now(UTC)
    delta = timedelta(days=random.randint(0, offset_days), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return now - delta

def make_meta():
    t = random_timestamp()
    return {
        "meta": {
            "created_at": t,
            "modified_at": t
        }
    }

async def seed():
    # 🔥 Delete old data
    await collections.messages.delete_many({})
    await collections.conversations.delete_many({})
    await collections.ads.delete_many({})
    await collections.pages.delete_many({})
    print("🧹 Old data deleted.")

    # 📄 Insert Pages
    page_ids = []
    for name in page_names:
        page = {
            "user_id": user_id,
            "name": name,
            "imageUrl": f"https://placekitten.com/{random.randint(60,70)}/{random.randint(60,70)}",
            "isDeleted": random.choice([True, False]),
            **make_meta()
        }
        result = await collections.pages.insert_one(page)
        page_ids.append(result.inserted_id)

    # 🏘 Insert Ads
    ad_ids = []
    for page_id in page_ids:
        ad_count = random.randint(1, 4)
        for _ in range(ad_count):
            ad = {
                "page_id": page_id,
                "name": random.choice(ad_names),
                "isDeleted": random.choice([True, False]),
                **make_meta()
            }
            result = await collections.ads.insert_one(ad)
            ad_ids.append(result.inserted_id)

    # 💬 Insert Conversations
    conversation_ids = []
    for ad_id in ad_ids:
        convo_count = random.randint(1, 3)
        for _ in range(convo_count):
            convo = {
                "ad_id": ad_id,
                "userName": random.choice(user_names),
                "userImage": f"https://placekitten.com/{random.randint(40,50)}/{random.randint(40,50)}",
                "lastActive": random_timestamp(),
                "unread": random.choice([True, False]),
                **make_meta()
            }
            result = await collections.conversations.insert_one(convo)
            conversation_ids.append(result.inserted_id)

    # 📥 Insert Messages
    for convo_id in conversation_ids:
        message = {
            "conversation_id": convo_id,
            "sender": "user",
            "text": random.choice(message_texts),
            "timestamp": random_timestamp(),
            **make_meta()
        }
        await collections.messages.insert_one(message)

    print("✅ Dummy data with structured meta fields seeded.")

if __name__ == "__main__":
    asyncio.run(seed())

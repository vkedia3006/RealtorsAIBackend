import asyncio
from datetime import datetime, timedelta
from core.database import collections  # using motor

# User ID
user_id = "7c947dd6-b12b-4ce1-b056-ffa3e8c42a92"

async def seed():
    # 1. Pages
    page1 = await collections.pages.insert_one({
        "user_id": user_id,
        "name": "Urban Realty Group",
        "imageUrl": "https://placekitten.com/64/64"
    })
    page1_id = page1.inserted_id

    page2 = await collections.pages.insert_one({
        "user_id": user_id,
        "name": "Coastal Properties",
        "imageUrl": "https://placekitten.com/65/65"
    })
    page2_id = page2.inserted_id

    # 2. Ads
    ad1 = await collections.ads.insert_one({
        "page_id": page1_id,
        "name": "Downtown Lofts"
    })
    ad1_id = ad1.inserted_id

    ad2 = await collections.ads.insert_one({
        "page_id": page1_id,
        "name": "Suburban Homes"
    })
    ad2_id = ad2.inserted_id

    ad3 = await collections.ads.insert_one({
        "page_id": page2_id,
        "name": "Oceanfront Condos"
    })
    ad3_id = ad3.inserted_id

    ad4 = await collections.ads.insert_one({
        "page_id": page2_id,
        "name": "Beach Houses"
    })
    ad4_id = ad4.inserted_id

    # 3. Conversations
    conv1 = await collections.conversations.insert_one({
        "ad_id": ad1_id,
        "userName": "John Smith",
        "userImage": "https://placekitten.com/40/40",
        "lastActive": datetime.utcnow(),
        "unread": True
    })
    conv1_id = conv1.inserted_id

    conv2 = await collections.conversations.insert_one({
        "ad_id": ad3_id,
        "userName": "Sarah Johnson",
        "userImage": "https://placekitten.com/41/41",
        "lastActive": datetime.utcnow() - timedelta(hours=1),
        "unread": False
    })
    conv2_id = conv2.inserted_id

    conv3 = await collections.conversations.insert_one({
        "ad_id": ad4_id,
        "userName": "Michael Brown",
        "userImage": "https://placekitten.com/42/42",
        "lastActive": datetime.utcnow() - timedelta(hours=2),
        "unread": True
    })
    conv3_id = conv3.inserted_id

    # 4. Messages
    await collections.messages.insert_many([
        {
            "conversation_id": conv1_id,
            "sender": "user",
            "text": "I'm interested in scheduling a viewing for the loft on Main Street.",
            "timestamp": datetime.utcnow()
        },
        {
            "conversation_id": conv2_id,
            "sender": "user",
            "text": "What are the HOA fees for these condos?",
            "timestamp": datetime.utcnow() - timedelta(hours=1)
        },
        {
            "conversation_id": conv3_id,
            "sender": "user",
            "text": "Do any of the chalets come with ski-in/ski-out access?",
            "timestamp": datetime.utcnow() - timedelta(hours=2)
        }
    ])

    print("✅ Dummy data seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed())

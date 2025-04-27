from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://vedantkedia001:Titanium@9876@cluster0.0ahkyxj.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = "sipcraft"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]
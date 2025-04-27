from motor.motor_asyncio import AsyncIOMotorClient
import os
from urllib.parse import quote_plus

MONGO_USER = quote_plus("vedant@user")
MONGO_PASS = quote_plus("p@ssw/rd123")

username = quote_plus("vedantkedia001")
password = quote_plus("Titanium@9876")
cluster = "cluster0.0ahkyxj.mongodb.net"
database_name = "sipcraft"

MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster}/{database_name}?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGO_URI)
db = client[database_name]
users_collection = db["users"]
from motor.motor_asyncio import AsyncIOMotorClient
import os
from urllib.parse import quote_plus
from types import SimpleNamespace

username = quote_plus("vedantkedia001")
password = quote_plus("Silver@9876")
cluster = "cluster0.0ahkyxj.mongodb.net"
database_name = "sipcraft"

MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster}/{database_name}?retryWrites=true&w=majority&ssl=true"

client = AsyncIOMotorClient(MONGO_URI)
db = client[database_name]

# Clean grouped access
collections = SimpleNamespace(
    users=db["users"],
    conversations=db["conversations"],
    messages=db["messages"],
    pages=db["pages"],
    ads=db["ads"]
)
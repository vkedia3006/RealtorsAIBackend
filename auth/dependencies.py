from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import decode_jwt_token
from core.database import users_collection

bearer_scheme = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_jwt_token(token)
    user_id = payload.get("user_id")
    
    print(payload)
    print(user_id)

    user = await users_collection.find_one({"facebook_id": user_id})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "facebook_id": user.get("facebook_id"),
        "name": user.get("name", "Facebook User")
    }

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import decode_jwt_token
from core.database import collections

bearer_scheme = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_jwt_token(token)
    user_id = payload.get("user_id")

    user = await collections.users.find_one({"user_id": str(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "user_id": user.get("user_id"),
        "name": user.get("name", "Facebook User"),
        "facebook_access_token": user.get("facebook_access_token")
    }
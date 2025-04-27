from fastapi import APIRouter, HTTPException, Depends
from jose import jwt, JWTError
from core.config import JWT_SECRET
from datetime import timedelta
from auth.jwt_handler import create_jwt_token

public_router = APIRouter()

@public_router.post("/refresh-token")
async def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_jwt_token(user_id, expires_delta=timedelta(minutes=15))
    return {"access_token": new_access_token}

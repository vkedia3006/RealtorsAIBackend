import jwt
from fastapi import HTTPException
from core.config import JWT_SECRET

def create_jwt_token(user_id: str):
    token = jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm="HS256")
    return token

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
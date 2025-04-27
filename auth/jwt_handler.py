from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from fastapi import HTTPException
from datetime import datetime, timedelta
from core.config import JWT_SECRET

def create_jwt_token(user_id: str, expires_delta: timedelta = timedelta(minutes=15)):
    expire = datetime.utcnow() + expires_delta
    to_encode = {"user_id": user_id, "exp": expire}
    token = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    return token

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

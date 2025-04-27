from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, RedirectResponse
from auth.facebook import get_facebook_login_url, exchange_code_for_token, save_user
from core.config import FRONTEND_URL
from auth.jwt_handler import create_jwt_token
from datetime import timedelta

public_router = APIRouter()

@public_router.post("/start-facebook-login")
async def start_facebook_login():
    fb_login_url = get_facebook_login_url()
    return JSONResponse(content={"fbLoginUrl": fb_login_url})

@public_router.get("/facebook-callback")
async def facebook_callback(code: str = Query(...)):
    token_data = exchange_code_for_token(code)
    
    access_token = token_data.get("access_token")
    
    facebook_id = await save_user(access_token)
    
    app_access_token = create_jwt_token(facebook_id, expires_delta=timedelta(minutes=15))
    app_refresh_token = create_jwt_token(facebook_id, expires_delta=timedelta(days=7))
    
    redirect_url = (
        f"{FRONTEND_URL}/login-success?"
        f"access_token={app_access_token}&"
        f"refresh_token={app_refresh_token}"
    )

    return RedirectResponse(redirect_url)

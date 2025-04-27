from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, RedirectResponse
from auth.facebook import get_facebook_login_url, exchange_code_for_token, save_user
from core.config import FRONTEND_URL

router = APIRouter()

@router.post("/start-facebook-login")
async def start_facebook_login():
    fb_login_url = get_facebook_login_url()
    return JSONResponse(content={"fbLoginUrl": fb_login_url})

@router.get("/facebook-callback")
async def facebook_callback(code: str = Query(...)):
    token_data = exchange_code_for_token(code)
    access_token = token_data.get("access_token")
    jwt_token = await save_user(access_token)
    return RedirectResponse(f"{FRONTEND_URL}/login-success?token={jwt_token}")

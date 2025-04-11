import requests
from fastapi import FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import urllib.parse

app = FastAPI()

FB_APP_ID = "636664199191003"
FB_APP_SECRET = "db457a2ea5cf9a2112e7e79bcf95115e"
FB_REDIRECT_URI = "https://api.sipcraftandco.com/facebook-callback"
VERIFY_TOKEN = "mysecrettoken123"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.sipcraftandco.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebhookData(BaseModel):
    object: str
    entry: list
    
@app.get("/")
async def read_root():
    return {"message": "Welcome to the homepage!"}    

@app.get("/api/test")
async def test():
    print("HELLO WORLD")
    return "Hello World!"



@app.post("/webhooks")
async def facebook_webhook(data: WebhookData):
    """Handles incoming webhook events from Facebook."""
    print("Received webhook:", data.dict())
    return {"status": "received"}

@app.get("/webhooks")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: int = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")
):
    """Facebook Webhook Verification."""
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=str(hub_challenge), status_code=status.HTTP_200_OK)

    return PlainTextResponse(content={"error": "Invalid token"}, status_code=status.HTTP_403_FORBIDDEN)

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: int = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")
):
    """Facebook Webhook Verification."""
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=str(hub_challenge), status_code=status.HTTP_200_OK)

    return PlainTextResponse(content={"error": "Invalid token"}, status_code=status.HTTP_403_FORBIDDEN)

@app.post("/start-facebook-login")
async def start_facebook_login():
    params = {
        "client_id": FB_APP_ID,
        "redirect_uri": FB_REDIRECT_URI,
        "scope": "email,public_profile",
        "response_type": "code",
        "state": "custom_state_token",  # optional
    }
    fb_login_url = f"https://www.facebook.com/v18.0/dialog/oauth?{urllib.parse.urlencode(params)}"
    return JSONResponse(content={"fbLoginUrl": fb_login_url})

@app.get("/facebook-callback")
async def facebook_callback(code: str, state: str = None):
    return {"message": "Logged in via Facebook", "code": code}
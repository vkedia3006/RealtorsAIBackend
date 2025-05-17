import urllib.parse
import requests
from core.config import FB_APP_ID, FB_APP_SECRET, FB_REDIRECT_URI
from core.database import collections
from auth.jwt_handler import create_jwt_token
import time
import uuid

def get_facebook_login_url():
    params = {
        "client_id": FB_APP_ID,
        "redirect_uri": FB_REDIRECT_URI,
        "scope": "pages_show_list,ads_management,leads_retrieval,pages_read_engagement",
        "response_type": "code",
        "state": "custom_state_token"
    }
    return f"https://www.facebook.com/v18.0/dialog/oauth?{urllib.parse.urlencode(params)}"

def exchange_code_for_token(code: str):
    params = {
        "client_id": FB_APP_ID,
        "redirect_uri": FB_REDIRECT_URI,
        "client_secret": FB_APP_SECRET,
        "code": code
    }
    response = requests.get("https://graph.facebook.com/v18.0/oauth/access_token", params=params)
    response.raise_for_status()
    data = response.json()
    access_token = data.get("access_token")
    
    long_lived_resp = requests.get(
        "https://graph.facebook.com/v18.0/oauth/access_token",
        params={
            "grant_type": "fb_exchange_token",
            "client_id": FB_APP_ID,
            "client_secret": FB_APP_SECRET,
            "fb_exchange_token": access_token
        }
    )
    long_lived_resp.raise_for_status()
    token_data = long_lived_resp.json()
    return token_data

async def save_user(access_token: str) -> str:
    user_info_resp = requests.get("https://graph.facebook.com/me", params={
        "access_token": access_token,
        "fields": "id,name,email"
    })
    user_info = user_info_resp.json()
    
    facebook_id = user_info["id"]
    name = user_info.get("name", "")
    email = user_info.get("email", "")

    expires_in_seconds = 60 * 24 * 60 * 60  # 60 days
    expires_at = int(time.time()) + expires_in_seconds

    existing_user = await collections.users.find_one({"facebook_id": facebook_id})

    if existing_user:
        await collections.users.update_one(
            {"facebook_id": facebook_id},
            {"$set": {
                "facebook_access_token": access_token,
                "facebook_access_token_expires_at": expires_at
            }}
        )
        return existing_user["user_id"]
    else:
        user_id = str(uuid.uuid4()) 
        await collections.users.insert_one({
            "user_id": user_id,
            "facebook_id": facebook_id,
            "facebook_access_token": access_token,
            "facebook_access_token_expires_at": expires_at,
            "name": name,
            "email": email
        })
        return user_id
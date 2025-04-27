import urllib.parse
import requests
from core.config import FB_APP_ID, FB_APP_SECRET, FB_REDIRECT_URI
from core.database import users_collection
from auth.jwt_handler import create_jwt_token

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

async def save_user(access_token: str):
    """Fetch Facebook user data and save to MongoDB."""
    user_info = requests.get(
        f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
    ).json()

    facebook_id = user_info["id"]
    email = user_info.get("email")
    name = user_info.get("name")

    existing_user = await users_collection.find_one({"facebook_id": facebook_id})
    if not existing_user:
        await users_collection.insert_one({
            "facebook_id": facebook_id,
            "email": email,
            "name": name
        })

    jwt_token = create_jwt_token(facebook_id)
    return jwt_token
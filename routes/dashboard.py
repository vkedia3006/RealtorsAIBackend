from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user

protected_router = APIRouter(dependencies=[Depends(get_current_user)])

@protected_router.get("/protected")
async def protected_example(user = Depends(get_current_user)):
    return {"message": f"Access granted to {user['facebook_id']}"}

@protected_router.get("/pages")
async def get_facebook_pages(user = Depends(get_current_user)):
    access_token = user.get("facebook_access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="Facebook access token not found")

    fb_response = requests.get(
        "https://graph.facebook.com/v19.0/me/accounts",
        params={"access_token": access_token}
    )

    if fb_response.status_code != 200:
        raise HTTPException(status_code=fb_response.status_code, detail="Failed to fetch pages from Facebook")

    pages_data = fb_response.json().get("data", [])
    return pages_data
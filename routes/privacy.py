from fastapi import APIRouter

public_router = APIRouter()

@public_router.get("/privacy")
async def privacy_policy():
    return {
        "title": "Privacy Policy",
        "message": "This is a placeholder privacy policy for sipcraftandco.com. We do not store any personal data."
    }
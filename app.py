from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.facebook_login import public_router as facebook_router
from routes.refresh_token import public_router as refresh_token_router
from routes.privacy import public_router as privacy_router
from routes.dashboard import protected_router as dashboard_router
from routes.webhook import public_router as webhook_router
from routes.lead import protected_router as lead_router

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.sipcraftandco.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public Routers
app.include_router(facebook_router, prefix="/public")
app.include_router(refresh_token_router, prefix="/public")
app.include_router(privacy_router, prefix="/public")
app.include_router(webhook_router, prefix="/public")

# Protected Routers
app.include_router(dashboard_router, prefix="/private")
app.include_router(lead_router, prefix="/private")

# Root
@app.get("/")
async def read_root():
    return {"message": "Welcome to the homepage!"}

@app.get("/api/test")
async def test():
    print("HELLO WORLD")
    return "Hello World!"

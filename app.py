from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import webhook, facebook_login, protected

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.sipcraftandco.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(facebook_login.router)
app.include_router(webhook.router)
app.include_router(protected.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the homepage!"}

@app.get("/api/test")
async def test():
    print("HELLO WORLD")
    return "Hello World!"

@app.get("/privacy")
async def privacy_policy():
    return {
        "title": "Privacy Policy",
        "message": "This is a placeholder privacy policy for sipcraftandco.com. We do not store any personal data."
    }

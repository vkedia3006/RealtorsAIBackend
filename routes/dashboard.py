from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user

protected_router = APIRouter(dependencies=[Depends(get_current_user)])

@protected_router.get("/dashboard")
async def dashboard(user = Depends(get_current_user)):
    return {"message": f"Welcome back, {user['name']}!"}

@protected_router.get("/protected")
async def protected_example(user = Depends(get_current_user)):
    return {"message": f"Access granted to {user['facebook_id']}"}
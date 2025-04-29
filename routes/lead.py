from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from auth.dependencies import get_current_user  # assuming same as your current auth setup
from llm.generator import generate_message 
from twilio_client.sender import send_sms

protected_router = APIRouter(dependencies=[Depends(get_current_user)])

class Lead(BaseModel):
    name: str
    phone: str
    email: str

@protected_router.post("/lead")
async def handle_lead(lead: Lead, user=Depends(get_current_user)):
    try:
        # Log who triggered it (optional)
        triggered_by = user.get("email", "Unknown user")

        # Generate message using LLM
        message = generate_message(lead.name)

        # Send via Twilio
        # send_sms(lead.phone, message)

        return {
            "status": "success",
            "sent_to": lead.phone,
            "message": message,
            "triggered_by": triggered_by
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

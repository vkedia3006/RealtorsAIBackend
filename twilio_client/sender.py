from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
from_number = os.getenv("TWILIO_PHONE_NUMBER")

def send_sms(to_number: str, message: str):
    twilio_client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )

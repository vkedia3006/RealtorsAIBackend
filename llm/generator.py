from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Grok (xAI) client
client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

def generate_message(name: str):
    try:
        response = client.chat.completions.create(
            model="grok-2-latest",
            messages=[
                {"role": "system", "content": "You are a helpful real estate assistant."},
                {"role": "user", "content": f"A new lead named {name} has shown interest in a property."},
                {"role": "user", "content": "Send a warm, professional welcome message via SMS."},
                {"role": "user", "content": "Keep it short, friendly, and human."}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Grok LLM error: {str(e)}")

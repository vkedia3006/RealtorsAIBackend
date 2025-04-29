import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_message(name: str):
    prompt = f"You are a realtor assistant. Write a warm, professional welcome message for a new lead named {name} who has just shown interest in a property."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful, friendly realtor assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message["content"].strip()
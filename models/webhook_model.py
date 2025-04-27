from pydantic import BaseModel

class WebhookData(BaseModel):
    object: str
    entry: list
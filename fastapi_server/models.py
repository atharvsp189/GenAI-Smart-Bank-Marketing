from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_input: str
    session_id: str

class Planner(BaseModel):
    target_audience: str

class Reflector(BaseModel):
    suggestions: str
    previous_strategy: str

class NotifiWriter(BaseModel):
    product_to_market: str
    customer_info: str
    guidelines: str

class EmailWriter(BaseModel):
    product_to_market: str
    customer_info: str
    guidelines: str

class SendEmail(BaseModel):
    receiver: str
    subject: str
    body: str

class SendNotification(BaseModel):
    receiver: str
    message: str
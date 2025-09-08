from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

class Notification(BaseModel):
    product: str = Field(description="Notification Focused on SIPs")

notifi_parser = JsonOutputParser(pydantic_object=Notification)


class Email(BaseModel):
    subject: str = Field(description="Subject of an email")
    body: str = Field(description="Body of an email")

email_parser = JsonOutputParser(pydantic_object=Email)
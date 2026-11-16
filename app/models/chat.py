from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        description="User message sent to the AI agent",
        min_length=1
    )
from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    username: str
    message: str


class MessageResponse(Message):
    created_at: datetime
    id: int
    message_counter: int

    class Config:
        from_attributes = True

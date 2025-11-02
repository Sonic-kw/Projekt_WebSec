"""
MongoDB Document Models using Beanie ODM
"""
from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime

class User(Document):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Settings:
        name = "users"

class ChatMessage(Document):
    username: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "chat_messages"
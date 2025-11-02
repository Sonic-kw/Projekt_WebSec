"""
Database initialization and connection management
"""
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGODB_URL, DATABASE_NAME
from schemas.models import User, ChatMessage

async def init_db():
    """Initialize database connection and Beanie ODM"""
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    await init_beanie(database=database, document_models=[User, ChatMessage])
    return client
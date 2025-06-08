import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from config.logging_config import logger

load_dotenv()

client = None
db = None

def init_mongodb():
    global client, db

    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("DATABASE_NAME", "test")

    if not mongodb_uri:
        logger.error("MONGODB_URI not set in environment")
        raise ValueError("MONGODB_URI not set in .env")

    client = AsyncIOMotorClient(mongodb_uri)
    db = client[db_name]
    logger.info(f"MongoDB connected to database: {db_name}")
    logger.info("MongoDB initialized successfully")

    return db

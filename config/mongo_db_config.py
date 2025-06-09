import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from config.logging_config import logger

# Load .env variables
load_dotenv()

client = None
db = None

def init_mongodb():
    global client, db

    mongodb_uri = os.getenv("URI")
    db_name = os.getenv("DB_NAME")

    logger.debug(f"Mongo URI: {mongodb_uri}")
    logger.debug(f"DB Name: {db_name}")

    if not mongodb_uri:
        logger.error("MONGODB_URI not set in environment")
        raise ValueError("MONGODB_URI not set in .env")

    client = AsyncIOMotorClient(mongodb_uri)
    db = client[db_name]
    logger.info(f"MongoDB connected to database: {db_name}")
    return db

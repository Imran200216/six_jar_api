import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
from config.logging_config import logger

def init_firebase():
    load_dotenv()
    firebase_cred_path = os.getenv("FIREBASE_CREDENTIAL_PATH")

    if not firebase_cred_path:
        logger.error("FIREBASE_CREDENTIAL_PATH not set in .env file")
        raise ValueError("FIREBASE_CREDENTIAL_PATH not set")

    if not os.path.exists(firebase_cred_path):
        logger.error(f"Credential file not found at: {firebase_cred_path}")
        raise FileNotFoundError(f"Credential file not found: {firebase_cred_path}")

    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_cred_path)
        firebase_admin.initialize_app(cred)
        logger.info("✅ Firebase Admin SDK initialized successfully")
    else:
        logger.info("Firebase already initialized")

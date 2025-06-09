import os
import httpx
from jose import jwt
from fastapi import APIRouter, HTTPException
from config.logging_config import logger
from config.mongo_db_config import db
from schemas.apple_auth.sign_in_model import SignInModel
from constants.collection_names import USERS_COLLECTION
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Apple config from environment
APPLE_KEYS_URL = os.getenv("APPLE_KEYS_URL")
APPLE_ISSUER = os.getenv("APPLE_ISSUER")
APPLE_AUDIENCE = os.getenv("APPLE_AUDIENCE")

# Apple auth router
router = APIRouter(tags=["Authentication 🔐"])


@router.post("/signInWithApple")
async def sign_in_with_apple(payload: SignInModel):
    try:
        identity_token = payload.identityToken
        logger.info("Received Apple identity token")

        # Get Apple's public keys
        async with httpx.AsyncClient() as client:
            resp = await client.get(APPLE_KEYS_URL)
            apple_keys = resp.json()["keys"]

        # Decode header to get key ID
        headers = jwt.get_unverified_header(identity_token)
        kid = headers["kid"]

        # Find the correct public key
        key = next((k for k in apple_keys if k["kid"] == kid), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid identity token")

        # Decode and verify identity token
        decoded = jwt.decode(
            identity_token,
            key,
            algorithms=["RS256"],
            audience=APPLE_AUDIENCE,
            issuer=APPLE_ISSUER,
        )

        logger.info(f"Apple token verified successfully: {decoded}")

        # Extract user details
        apple_user_id = decoded["sub"]
        email = decoded.get("email")

        # Check or create user in MongoDB
        user = await db[USERS_COLLECTION].find_one({"apple_user_id": apple_user_id})
        if not user:
            await db[USERS_COLLECTION].insert_one(
                {"apple_user_id": apple_user_id, "email": email}
            )

        return {
            "message": "Apple sign-in successful",
            "userId": apple_user_id,
            "email": email,
        }

    except jwt.JWTError as e:
        logger.error(f"JWT Error during Apple Sign-In: {e}")
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        logger.error(f"Apple Sign-In failed: {e}")
        raise HTTPException(status_code=500, detail="Apple sign-in failed")

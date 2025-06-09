from fastapi import APIRouter, HTTPException, Request
from firebase_admin import auth
from config.logging_config import logger
from config.mongo_db_config import db
from constants.collection_names import USERS_COLLECTION


# email_auth router
router = APIRouter(tags=["Authentication 🔐"])


# Sign in with google
@router.post("/signInWithGoogle")
async def sign_in_with_google(request: Request):
    try:
        body = await request.json()
        id_token = body.get("idToken")

        if not id_token:
            raise HTTPException(status_code=400, detail="idToken is required")

        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        picture = decoded_token.get("picture")

        logger.info(f"Verified Google user: {email} (UID={uid})")

        # Optional: store user in MongoDB if not exists
        user_data = {
            "firebase_uid": uid,
            "userEmail": email,
            "userName": name,
            "photoURL": picture,
        }
        await db[USERS_COLLECTION].update_one(
            {"firebase_uid": uid}, {"$setOnInsert": user_data}, upsert=True
        )

        return {
            "message": "Google Sign-In verified successfully",
            "uid": uid,
            "email": email,
            "name": name,
            "photoURL": picture,
        }

    except Exception as e:
        logger.error(f"Google Sign-In verification failed: {str(e)}")
        raise HTTPException(
            status_code=401, detail=f"Token verification failed: {str(e)}"
        )

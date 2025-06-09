from fastapi import APIRouter, HTTPException
from schemas.email_auth.sign_up_model import SignUpModel
from schemas.email_auth.forget_password_model import ForgetPasswordModel
from schemas.email_auth.sign_in_model import SignInModel
from config.logging_config import logger
from firebase_admin import auth
from config.mongo_db_config import db
from models.user_model import UserModel
from constants.collection_names import USERS_COLLECTION

import requests
import os


# email_auth router
router = APIRouter(tags=["Authentication 🔐"])

# Firebae Web Api Key
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")


# SignUp With Email Password
@router.post("/signUpWithEmailPassword")
async def signUpWithEmailPassword(user: SignUpModel):
    try:
        logger.info(f"Attempting to create user with email: {user.userEmail}")

        # create user in firebase (blocking call)
        firebase_user = auth.create_user(
            email=user.userEmail,
            password=user.userPassword,
            display_name=user.userName,
        )

        logger.info(f"User created successfully in Firebase: UID={firebase_user.uid}")

        # store user in mongodb asynchronously
        user_data = UserModel(
            firebase_uid=firebase_user.uid,
            userName=user.userName,
            userEmail=user.userEmail,
        )

        await db[USERS_COLLECTION].insert_one(user_data.dict())
        logger.info(f"User data inserted into MongoDB for UID={firebase_user.uid}")

        return {"message": "User created successfully", "uid": firebase_user.uid}

    except auth.EmailAlreadyExistsError:
        logger.warning(f"Email already in use: {user.userEmail}")
        raise HTTPException(status_code=400, detail="Email already in use")

    except Exception as e:
        logger.error(f"SignUp failed for {user.userEmail}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"SignUp failed: {str(e)}")


@router.post("/signInWithEmailPassword")
async def signInWithEmailPassword(user: SignInModel):
    logger.info(f"Attempting to sign in user with email: {user.userEmail}")

    try:
        if not FIREBASE_WEB_API_KEY:
            logger.error("FIREBASE_WEB_API_KEY not set in .env")
            raise HTTPException(status_code=500, detail="Firebase Web API Key missing")

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

        payload = {
            "email": user.userEmail,
            "password": user.userPassword,
            "returnSecureToken": True,
        }

        response = requests.post(url, json=payload)
        res_data = response.json()

        if response.status_code != 200:
            error_message = res_data.get("error", {}).get(
                "message", "Authentication failed"
            )
            logger.warning(f"Sign-in failed for {user.userEmail}: {error_message}")
            raise HTTPException(
                status_code=400, detail=f"Sign-in failed: {error_message}"
            )

        logger.info(f"User signed in successfully: {user.userEmail}")
        return {
            "message": "User signed in successfully",
            "idToken": res_data["idToken"],
            "refreshToken": res_data["refreshToken"],
            "expiresIn": res_data["expiresIn"],
            "firebase_uid": res_data["localId"],
        }

    except Exception as e:
        logger.error(f"Sign-in error for {user.userEmail}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Sign-in failed: {str(e)}")


# Forget Password
@router.post("/forgetPassword")
def forgetPassword(user: ForgetPasswordModel):
    try:
        logger.info(
            f"Attempting to send Forget Password Link to user with email: {user.userEmail}"
        )

        reset_link = auth.generate_password_reset_link(user.userEmail)

        logger.info(f"Password reset link generated for {user.userEmail}")
        return {
            "message": "Password reset link generated successfully",
            "resetLink": reset_link,
        }

    except auth.UserNotFoundError:
        logger.warning(f"No user found with email: {user.userEmail}")
        raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        logger.error(
            f"Failed to generate password reset link for {user.userEmail}: {str(e)}"
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to generate reset link: {str(e)}"
        )
